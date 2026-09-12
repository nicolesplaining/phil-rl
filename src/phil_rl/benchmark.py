"""Frozen source-only evaluations. References never enter the model request."""

import json
from pathlib import Path

from phil_rl.schema import (
    Artifact,
    Claim,
    Evidence,
    Formalization,
    Reconstruction,
    Relation,
    Symbol,
    Translation,
    fingerprint,
)
from phil_rl.source import source_units


def reference(case: dict) -> Artifact | None:
    if "claims" not in case:
        return None
    units = {u.id: u for u in source_units(case["source"])}
    symbols = []
    for name, value in case["symbols"].items():
        if isinstance(value, str):
            kind, arity, meaning = "proposition", 0, value
        else:
            arity, meaning = value
            kind = "predicate" if arity else "constant"
        symbols.append(Symbol(name=name, kind=kind, arity=arity, meaning=meaning))
    claims = [
        Claim(
            id=f"r{i}",
            text=units[unit].text,
            role=role,
            origin="explicit",
            evidence=Evidence(
                quote=units[unit].text,
                occurrence=sum(
                    u.text == units[unit].text and u.start < units[unit].start
                    for u in units.values()
                ),
            ),
            interpretation_note="Pre-inference engineering reference.",
        )
        for i, (unit, role, _) in enumerate(case["claims"], 1)
    ]
    conclusion = next(c.id for c in claims if c.role == "conclusion")
    premises = [c.id for c in claims if c.role == "premise"]
    reconstruction = Reconstruction(
        title=case["id"],
        claims=claims,
        relations=[Relation(premises=premises, conclusion=conclusion, kind="supports")],
        conclusion_id=conclusion,
        ambiguities=[],
    )
    formalization = Formalization(
        logic=case["logic"],
        domain_description="Nonempty domain of individuals.",
        symbols=symbols,
        translations=[
            Translation(claim_id=c.id, formula=entry[2], reason="")
            for c, entry in zip(claims, case["claims"], strict=True)
        ],
        interpretation_notes=["Reference labels are withheld from the evaluated model."],
    )
    return Artifact.create(case["source"], reconstruction, formalization)


def load_suite(path: Path) -> dict:
    suite = json.loads(path.read_text())
    ids = [c["id"] for c in suite["cases"]]
    if not ids or len(ids) != len(set(ids)) or any(not i.isalnum() for i in ids):
        raise ValueError("Suite requires unique alphanumeric case identifiers.")
    for case in suite["cases"]:
        reference(case)
    return suite


def _generate_case(config, source):
    from phil_rl.client import ChatClient, GenerationError
    from phil_rl.pipeline import run

    try:
        artifact, trace = run(source, ChatClient(config))
        return artifact, trace, None
    except GenerationError as error:
        return (
            None,
            getattr(error, "trace", None),
            {
                "error": str(error),
                "attempts": error.attempts,
            },
        )


def evaluate_suite(client, directory: Path, suite_path: Path, workers: int = 1, cases=None):
    # Import here to keep CLI serialization in one place without a module cycle.
    import sys
    from concurrent.futures import ProcessPoolExecutor, as_completed
    from multiprocessing import get_context

    from phil_rl.cli import save, write_json

    suite = load_suite(suite_path)
    selected = suite["cases"]
    if cases is not None:
        if len(set(cases)) != len(cases) or not set(cases) <= {c["id"] for c in selected}:
            raise ValueError("Select unique case ids from the suite.")
        selected = [c for c in selected if c["id"] in cases]
    if not 1 <= workers <= 4:
        raise ValueError("Use one through four evaluation workers.")
    directory.mkdir(parents=True, exist_ok=False)
    write_json(directory / "suite.json", suite)
    rows = []
    # Separate processes also isolate Z3 contexts; sharing its default context
    # between concurrent Python threads is unsafe.
    with ProcessPoolExecutor(max_workers=workers, mp_context=get_context("spawn")) as pool:
        pending = {
            pool.submit(_generate_case, client.config, case["source"]): case for case in selected
        }
        for future in as_completed(pending):
            case = pending[future]
            artifact, trace, failure = future.result()
            print(f"Completed {case['id']}...", file=sys.stderr, flush=True)
            row = {"case": case["id"], "expected": case["status"]}
            if failure is None:
                checks = save(directory / case["id"], artifact, trace)
                row.update(
                    generated=True,
                    actual=checks["explicit"]["status"],
                    ambiguity_recorded=bool(artifact and artifact.reconstruction.ambiguities),
                )
            else:
                failed = directory / case["id"]
                failed.mkdir()
                write_json(failed / "failure.json", failure)
                if trace:
                    write_json(failed / "trace.json", trace)
                row.update(generated=False, actual="generation_failed", error=failure["error"])
            rows.append(row)
            result = {
                "suite_version": suite["version"],
                "suite_sha256": fingerprint(suite),
                "model_config": client.config.public(),
                "workers": workers,
                "total": len(selected),
                "selected_cases": [c["id"] for c in selected],
                "completed": len(rows),
                "cases": sorted(rows, key=lambda r: r["case"]),
                "fidelity": "not_assessed",
                "note": "Review source meaning and symbol alignment before scoring fidelity.",
            }
            write_json(directory / "summary.json", result)
    return result
