import argparse
import json
import os
import sys
from pathlib import Path

from phil_rl.client import ChatClient, GenerationError, ModelConfig
from phil_rl.examples import fixtures
from phil_rl.lean import check_lean, export
from phil_rl.pipeline import PipelineError, run
from phil_rl.report import review
from phil_rl.schema import Artifact, Formalization
from phil_rl.source import GroundedReconstruction
from phil_rl.verify import check


def write_json(path: Path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def load(path: Path) -> Artifact:
    return Artifact.model_validate_json(path.read_text())


def save_failure(directory: Path, error: GenerationError):
    directory.mkdir(parents=True, exist_ok=False)
    write_json(directory / "failure.json", {"error": str(error), "attempts": error.attempts})
    if isinstance(error, PipelineError):
        write_json(directory / "trace.json", error.trace)


def save(directory: Path, artifact: Artifact | None, trace: dict):
    directory.mkdir(parents=True, exist_ok=False)
    if artifact is None:
        result = {
            "status": trace["outcome"],
            "reason": trace["reason"],
            "included_premise_ids": [],
            "fidelity": "not_assessed",
        }
        checks = {"explicit": result, "with_proposed_implicit": result}
        write_json(directory / "trace.json", trace)
        write_json(directory / "checks.json", checks)
        return checks
    write_json(directory / "argument.json", artifact.model_dump(mode="json"))
    write_json(directory / "trace.json", trace)
    checks = {"explicit": check(artifact), "with_proposed_implicit": check(artifact, True)}
    write_json(directory / "checks.json", checks)
    (directory / "review.md").write_text(review(artifact, checks, trace["provenance"]))
    if checks["explicit"]["status"] != "unsupported":
        (directory / "Statement.lean").write_text(export(artifact))
    return checks


def model_arguments(parser):
    parser.add_argument(
        "--base-url", default=os.getenv("PHIL_BASE_URL", "http://127.0.0.1:8000/v1")
    )
    parser.add_argument("--model", default=os.getenv("PHIL_MODEL", "Qwen/Qwen3-32B"))
    parser.add_argument("--max-tokens", type=int, default=8192)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--transport-retries", type=int, default=2)
    parser.add_argument("--timeout", type=float, default=360)
    parser.add_argument("--no-structured", action="store_true")
    parser.add_argument("--no-qwen-template", action="store_true")
    parser.add_argument(
        "--no-thinking", action="store_true", help="Disable Qwen thinking for an ablation."
    )


def model_config(args):
    return ModelConfig(
        base_url=args.base_url,
        model=args.model,
        api_key=os.getenv("PHIL_API_KEY"),
        max_tokens=args.max_tokens,
        retries=args.retries,
        transport_retries=args.transport_retries,
        timeout=args.timeout,
        structured=not args.no_structured,
        qwen_nonthinking=args.no_thinking and not args.no_qwen_template,
    )


def evaluate(client: ChatClient, directory: Path, names: list[str]) -> dict:
    references = fixtures()
    if not names or len(names) != len(set(names)) or any(n not in references for n in names):
        raise ValueError("Choose unique case names from the synthetic fixture suite.")
    directory.mkdir(parents=True, exist_ok=False)
    rows = []
    for name in names:
        reference, expected, expected_augmented = references[name]
        print(f"Evaluating {name}...", file=sys.stderr, flush=True)
        row = {
            "case": name,
            "expected_explicit": expected,
            "expected_augmented": expected_augmented,
        }
        try:
            artifact, trace = run(reference.source, client)
            checks = save(directory / name, artifact, trace)
            row.update(
                {
                    "generated": True,
                    "actual_explicit": checks["explicit"]["status"],
                    "actual_augmented": checks["with_proposed_implicit"]["status"],
                    "status_match": checks["explicit"]["status"] == expected,
                    "augmented_status_match": checks["with_proposed_implicit"]["status"]
                    == expected_augmented,
                    "reconstruction_attempts": len(trace["reconstruction_attempts"]),
                    "formalization_attempts": len(trace["formalization_attempts"]),
                }
            )
        except GenerationError as error:
            row.update(
                {
                    "generated": False,
                    "error": str(error),
                    "status_match": False,
                    "augmented_status_match": False,
                }
            )
            save_failure(directory / name, error)
        rows.append(row)
        result = {
            "provenance": "llm_on_original_synthetic_passages",
            "model_config": client.config.public(),
            "cases": rows,
            "total": len(names),
            "completed": len(rows),
            "generated": sum(r["generated"] for r in rows),
            "explicit_status_matches": sum(r["status_match"] for r in rows),
            "augmented_status_matches": sum(r["augmented_status_match"] for r in rows),
            "fidelity": "not_assessed",
            "note": "Status agreement does not establish fidelity or philosophical quality.",
        }
        write_json(directory / "summary.json", result)
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Reconstruct and formalize short philosophical arguments."
    )
    sub = parser.add_subparsers(dest="command", required=True)
    demo = sub.add_parser("demo", help="Run manually specified synthetic fixtures without an LLM.")
    demo.add_argument("--out", type=Path, required=True)
    schema = sub.add_parser("schema", help="Print a model-stage JSON schema.")
    schema.add_argument("stage", choices=["reconstruction", "formalization"])
    generate = sub.add_parser("run", help="Use two LLM calls: reconstruction then formalization.")
    generate.add_argument("input", type=Path)
    generate.add_argument("--out", type=Path, required=True)
    model_arguments(generate)
    evaluation = sub.add_parser(
        "evaluate", help="Run an LLM on synthetic passages and report failures."
    )
    evaluation.add_argument("--out", type=Path, required=True)
    evaluation.add_argument(
        "--cases", nargs="+", choices=list(fixtures()), default=list(fixtures())
    )
    model_arguments(evaluation)
    benchmark = sub.add_parser("benchmark", help="Evaluate only source text from a frozen suite.")
    benchmark.add_argument("--suite", type=Path, required=True)
    benchmark.add_argument("--out", type=Path, required=True)
    benchmark.add_argument("--workers", type=int, default=1)
    model_arguments(benchmark)
    validate = sub.add_parser("check", help="Check an existing frozen artifact with Z3.")
    validate.add_argument("artifact", type=Path)
    validate.add_argument("--include-implicit", action="store_true")
    validate.add_argument("--timeout-ms", type=int, default=5000)
    lean = sub.add_parser("lean", help="Export a Lean statement or a small propositional proof.")
    lean.add_argument("artifact", type=Path)
    lean.add_argument("--out", type=Path, required=True)
    lean.add_argument("--include-implicit", action="store_true")
    lean.add_argument("--prove", action="store_true")
    lean.add_argument("--check", action="store_true", dest="check_lean")
    lean.add_argument("--lean-bin", default="lean")
    args = parser.parse_args(argv)
    try:
        if args.command == "schema":
            model = GroundedReconstruction if args.stage == "reconstruction" else Formalization
            print(json.dumps(model.model_json_schema(), indent=2))
        elif args.command == "demo":
            args.out.mkdir(parents=True, exist_ok=False)
            rows = []
            for name, (artifact, expected, augmented) in fixtures().items():
                checks = save(args.out / name, artifact, {"provenance": "manual_synthetic_fixture"})
                actual, actual_augmented = (
                    checks["explicit"]["status"],
                    checks["with_proposed_implicit"]["status"],
                )
                rows.append(
                    {
                        "case": name,
                        "expected": expected,
                        "actual": actual,
                        "expected_augmented": augmented,
                        "actual_augmented": actual_augmented,
                        "passed": actual == expected and actual_augmented == augmented,
                    }
                )
            result = {
                "provenance": "manual_synthetic_fixtures",
                "cases": rows,
                "passed": sum(r["passed"] for r in rows),
                "total": len(rows),
                "note": "Engineering checks, not evidence of LLM translation quality.",
            }
            write_json(args.out / "summary.json", result)
            print(json.dumps(result, indent=2))
            return 0 if all(r["passed"] for r in rows) else 1
        elif args.command == "run":
            if args.out.exists():
                raise ValueError("Output directory exists; choose a new run directory.")
            try:
                artifact, trace = run(args.input.read_text(), ChatClient(model_config(args)))
            except GenerationError as error:
                save_failure(args.out, error)
                raise
            print(json.dumps(save(args.out, artifact, trace), indent=2))
        elif args.command == "evaluate":
            result = evaluate(ChatClient(model_config(args)), args.out, args.cases)
            print(json.dumps(result, indent=2))
            return 0 if result["generated"] == result["total"] else 1
        elif args.command == "benchmark":
            from phil_rl.benchmark import evaluate_suite

            result = evaluate_suite(
                ChatClient(model_config(args)), args.out, args.suite, args.workers
            )
            print(json.dumps(result, indent=2))
            return 0 if all(row["generated"] for row in result["cases"]) else 1
        elif args.command == "check":
            print(
                json.dumps(
                    check(load(args.artifact), args.include_implicit, args.timeout_ms), indent=2
                )
            )
        elif args.command == "lean":
            if args.out.exists():
                raise ValueError("Output file exists; choose a new filename.")
            code = export(load(args.artifact), args.include_implicit, args.prove)
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(code)
            if args.check_lean:
                result = check_lean(code, args.lean_bin)
                print(json.dumps(result, indent=2))
                return 0 if result["status"] == "passed" else 1
            print(f"Wrote {args.out}. Lean has not checked this file.")
    except (ValueError, OSError, GenerationError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
