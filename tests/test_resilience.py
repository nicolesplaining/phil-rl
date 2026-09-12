import json

import httpx
import pytest

from phil_rl.cli import save, save_failure
from phil_rl.client import ChatClient, GenerationError, ModelConfig
from phil_rl.pipeline import PipelineError, run
from phil_rl.source import GroundedReconstruction

NO_ARGUMENT = {
    "status": "no_argument",
    "reason": "A question without premises or a conclusion.",
    "title": "A question",
    "claims": [],
    "relations": [],
    "conclusion_id": None,
    "ambiguities": [],
}


def completion(content, finish="stop"):
    return httpx.Response(
        200,
        json={
            "choices": [
                {
                    "finish_reason": finish,
                    "message": {"content": content, "reasoning": "test reasoning"},
                }
            ]
        },
    )


def test_no_argument_stops_after_reconstruction_and_is_saved(tmp_path):
    calls = []

    def handler(request):
        calls.append(request)
        return completion(json.dumps(NO_ARGUMENT))

    artifact, trace = run(
        "What is justice?", ChatClient(ModelConfig(), httpx.MockTransport(handler))
    )
    assert artifact is None and len(calls) == 1
    checks = save(tmp_path / "run", artifact, trace)
    assert checks["explicit"]["status"] == "no_argument"
    assert trace["reconstruction_attempts"][0]["reasoning"] == "test reasoning"
    assert not (tmp_path / "run" / "Statement.lean").exists()


@pytest.mark.parametrize("field,value", [("reason", ""), ("conclusion_id", "c1")])
def test_no_argument_requires_consistent_outcome(field, value):
    with pytest.raises(ValueError):
        GroundedReconstruction.model_validate({**NO_ARGUMENT, field: value})


@pytest.mark.parametrize("source", ["", "  ", "x" * 20001, "X. " * 257])
def test_invalid_input_never_calls_model(source):
    def handler(request):
        pytest.fail("Invalid input made a model request")

    with pytest.raises(ValueError):
        run(source, ChatClient(ModelConfig(), httpx.MockTransport(handler)))


def test_transient_error_retries_same_request_and_preserves_failure(monkeypatch):
    monkeypatch.setattr("phil_rl.client.time.sleep", lambda _: None)
    requests = []

    def handler(request):
        requests.append(request.content)
        return (
            httpx.Response(503, text="private server detail")
            if len(requests) == 1
            else completion(json.dumps(NO_ARGUMENT))
        )

    _, attempts = ChatClient(ModelConfig(), httpx.MockTransport(handler)).generate(
        GroundedReconstruction, "test", {}
    )
    assert requests[0] == requests[1]
    assert [r["accepted"] for r in attempts] == [False, True]
    assert "private server detail" not in json.dumps(attempts)


def test_transport_retry_budget_and_safe_error(monkeypatch):
    monkeypatch.setattr("phil_rl.client.time.sleep", lambda _: None)

    def handler(request):
        raise httpx.ReadTimeout("secret URL")

    with pytest.raises(GenerationError) as caught:
        ChatClient(ModelConfig(transport_retries=1), httpx.MockTransport(handler)).generate(
            GroundedReconstruction, "test", {}
        )
    assert len(caught.value.attempts) == 2
    assert "secret" not in json.dumps(caught.value.attempts)


@pytest.mark.parametrize(
    "reply",
    [
        completion('{"partial":', "length"),
        httpx.Response(200, json={"choices": []}),
        httpx.Response(200, text="bad JSON"),
    ],
)
def test_incomplete_attempts_are_preserved(reply):
    with pytest.raises(GenerationError) as caught:
        ChatClient(ModelConfig(), httpx.MockTransport(lambda _: reply)).generate(
            GroundedReconstruction, "test", {}
        )
    assert len(caught.value.attempts) == 1
    assert not caught.value.attempts[0]["accepted"]


def test_formalization_failure_preserves_frozen_reconstruction(tmp_path):
    draft = {
        "status": "argument",
        "reason": "",
        "title": "Circular",
        "claims": [
            {
                "id": "p",
                "text": "Justice matters.",
                "role": "premise",
                "origin": "explicit",
                "evidence_ids": ["s1"],
                "interpretation_note": "",
            },
            {
                "id": "c",
                "text": "Justice matters.",
                "role": "conclusion",
                "origin": "explicit",
                "evidence_ids": ["s2"],
                "interpretation_note": "",
            },
        ],
        "relations": [{"premises": ["p"], "conclusion": "c", "kind": "supports"}],
        "conclusion_id": "c",
        "ambiguities": [],
    }
    replies = iter([completion(json.dumps(draft)), completion("{", "length")])
    client = ChatClient(ModelConfig(), httpx.MockTransport(lambda _: next(replies)))
    with pytest.raises(PipelineError) as caught:
        run("Justice matters. Therefore justice matters.", client)
    error = caught.value
    assert error.trace["failed_stage"] == "formalization"
    assert len(error.trace["frozen_reconstruction"]["claims"]) == 2
    assert error.trace["formalization_attempts"][0]["response"] == "{"
    save_failure(tmp_path / "failed", error)
    assert (tmp_path / "failed" / "trace.json").exists()
