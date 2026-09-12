import json

import httpx
import pytest

from phil_rl.cli import main
from phil_rl.client import ChatClient, GenerationError, ModelConfig
from phil_rl.examples import fixtures
from phil_rl.pipeline import run
from phil_rl.schema import Artifact, Formalization, Reconstruction, fingerprint


def response(content, finish="stop"):
    return httpx.Response(
        200, json={"choices": [{"finish_reason": finish, "message": {"content": content}}]}
    )


def test_two_stage_http_pipeline_freezes_claims_and_does_not_send_solver_feedback():
    reference = fixtures()["affirming_consequent"][0]
    requests = []

    def handler(request):
        body = json.loads(request.content)
        requests.append(body)
        if len(requests) == 1:
            return response(reference.reconstruction.model_dump_json())
        assert (
            json.loads(body["messages"][1]["content"])["frozen_reconstruction"]
            == reference.reconstruction.model_dump()
        )
        return response(reference.formalization.model_dump_json())

    client = ChatClient(ModelConfig(api_key="test-secret"), httpx.MockTransport(handler))
    artifact, trace = run(reference.source, client)
    assert len(requests) == 2
    assert artifact == reference
    assert trace["explicit_check"]["status"] == "invalid"
    assert "test-secret" not in json.dumps(trace)
    assert trace["provenance"] == "llm_generated"
    assert all("solver" not in json.loads(r["messages"][1]["content"]) for r in requests)
    assert all(r["response_format"]["type"] == "json_schema" for r in requests)


def test_structural_retry_for_fabricated_source_quote():
    reference = fixtures()["modus_ponens"][0]
    fabricated = reference.reconstruction.model_dump()
    fabricated["claims"][0]["evidence"]["quote"] = "The source never said this."
    replies = iter([json.dumps(fabricated), reference.reconstruction.model_dump_json()])
    client = ChatClient(ModelConfig(), httpx.MockTransport(lambda request: response(next(replies))))
    reconstruction, attempts = client.generate(
        Reconstruction,
        "test",
        {"source": reference.source},
        validate=lambda result: result.validate_source(reference.source),
    )
    assert reconstruction == reference.reconstruction
    assert [a["accepted"] for a in attempts] == [False, True]


def test_rejects_silent_claim_additions():
    reference = fixtures()["modus_ponens"][0]
    data = reference.formalization.model_dump()
    data["translations"].append({"claim_id": "extra", "formula": "F", "reason": ""})
    with pytest.raises(ValueError, match="exactly once"):
        Artifact.create(
            reference.source, reference.reconstruction, Formalization.model_validate(data)
        )


def test_rejects_support_cycles_and_explicit_claims_without_evidence():
    original = fixtures()["modus_ponens"][0].reconstruction.model_dump()
    original["relations"].append({"premises": ["c3"], "conclusion": "c1", "kind": "supports"})
    with pytest.raises(ValueError, match="acyclic"):
        Reconstruction.model_validate(original)
    original = fixtures()["modus_ponens"][0].reconstruction.model_dump()
    original["claims"][0]["evidence"] = None
    with pytest.raises(ValueError, match="evidence"):
        Reconstruction.model_validate(original)


def test_rejects_digest_preserving_but_invalid_formalization():
    data = fixtures()["modus_ponens"][0].model_dump()
    data["formalization"]["translations"][0]["formula"] = "(implies F unknown)"
    data["formalization_sha256"] = fingerprint(data["formalization"])
    with pytest.raises(ValueError, match="Undeclared"):
        Artifact.model_validate(data)


def test_http_errors_do_not_leak_response_bodies_or_credentials():
    client = ChatClient(
        ModelConfig(api_key="secret"),
        httpx.MockTransport(lambda request: httpx.Response(401, text="secret")),
    )
    with pytest.raises(GenerationError, match="HTTP 401") as error:
        client.generate(Reconstruction, "test", {})
    assert "secret" not in str(error.value)


@pytest.mark.parametrize("content,finish", [("{}", "length"), ("", "stop"), (None, "stop")])
def test_incomplete_generation_fails(content, finish):
    client = ChatClient(
        ModelConfig(), httpx.MockTransport(lambda request: response(content, finish))
    )
    with pytest.raises(GenerationError):
        client.generate(Reconstruction, "test", {})


def test_invalid_json_has_bounded_retries():
    calls = []

    def handler(request):
        calls.append(request)
        return response("not JSON")

    client = ChatClient(ModelConfig(retries=1), httpx.MockTransport(handler))
    with pytest.raises(GenerationError, match="after 2 attempts"):
        client.generate(Reconstruction, "test", {})
    assert len(calls) == 2


def test_demo_cli_and_no_overwrite(tmp_path):
    directory = tmp_path / "demo"
    assert main(["demo", "--out", str(directory)]) == 0
    summary = json.loads((directory / "summary.json").read_text())
    assert summary["passed"] == summary["total"] == 9
    assert main(["demo", "--out", str(directory)]) == 1
    assert main(["check", str(directory / "modus_ponens" / "argument.json")]) == 0


def test_lean_missing_executable_is_not_a_pass(tmp_path):
    from phil_rl.lean import check_lean, export

    result = check_lean(export(fixtures()["modus_ponens"][0]), str(tmp_path / "absent-lean"))
    assert result["status"] == "unavailable"
    assert not result.get("proof_checked", False)


def test_schema_validator_errors_can_be_retried():
    reference = fixtures()["modus_ponens"][0]
    missing = reference.reconstruction.model_dump()
    missing["claims"][0]["evidence"] = None
    replies = iter([json.dumps(missing), reference.reconstruction.model_dump_json()])
    client = ChatClient(ModelConfig(), httpx.MockTransport(lambda request: response(next(replies))))
    reconstruction, attempts = client.generate(Reconstruction, "test", {})
    assert reconstruction == reference.reconstruction
    assert attempts[0]["accepted"] is False


def test_evaluation_records_failures_and_withholds_references(tmp_path):
    from phil_rl.cli import evaluate

    reference = fixtures()["modus_ponens"][0]
    replies = iter(
        [
            reference.reconstruction.model_dump_json(),
            reference.formalization.model_dump_json(),
            "{}",
        ]
    )
    requests = []

    def handler(request):
        body = json.loads(request.content)
        requests.append(json.loads(body["messages"][1]["content"]))
        return response(next(replies))

    client = ChatClient(ModelConfig(retries=0), httpx.MockTransport(handler))
    result = evaluate(client, tmp_path / "evaluation", ["modus_ponens", "modal"])
    assert result["generated"] == result["explicit_status_matches"] == 1
    assert result["total"] == result["completed"] == 2
    assert all("expected" not in item and "reference" not in item for item in requests)
    assert (tmp_path / "evaluation" / "modal" / "failure.json").exists()
    report = (tmp_path / "evaluation" / "modus_ponens" / "review.md").read_text()
    assert "not assessed" in report
    assert "(implies R F)" in report


def test_server_script_defaults_to_gpu_one(tmp_path):
    import subprocess
    from pathlib import Path

    # Shell syntax check only; no server or GPU process is started in tests.
    path = Path(__file__).parents[1] / "scripts" / "serve.sh"
    subprocess.run(["bash", "-n", str(path)], check=True)
    assert "export CUDA_VISIBLE_DEVICES=1" in path.read_text()
    assert "--tensor-parallel-size 1" in path.read_text()
