import argparse
import json
import os
import sys
from pathlib import Path

from phil_rl.client import ChatClient, GenerationError, ModelConfig
from phil_rl.examples import fixtures
from phil_rl.lean import check_lean, export
from phil_rl.pipeline import run
from phil_rl.schema import Artifact, Formalization, Reconstruction
from phil_rl.verify import check


def write_json(path: Path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def load(path: Path) -> Artifact:
    return Artifact.model_validate_json(path.read_text())


def save(directory: Path, artifact: Artifact, trace: dict):
    directory.mkdir(parents=True, exist_ok=False)
    write_json(directory / "argument.json", artifact.model_dump(mode="json"))
    write_json(directory / "trace.json", trace)
    checks = {"explicit": check(artifact), "with_proposed_implicit": check(artifact, True)}
    write_json(directory / "checks.json", checks)
    if checks["explicit"]["status"] != "unsupported":
        (directory / "Statement.lean").write_text(export(artifact))
    return checks


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
    generate.add_argument(
        "--base-url", default=os.getenv("PHIL_BASE_URL", "http://127.0.0.1:8000/v1")
    )
    generate.add_argument("--model", default=os.getenv("PHIL_MODEL", "Qwen/Qwen3-32B"))
    generate.add_argument("--max-tokens", type=int, default=8192)
    generate.add_argument("--retries", type=int, default=2)
    generate.add_argument("--timeout", type=float, default=180)
    generate.add_argument("--no-structured", action="store_true")
    generate.add_argument("--no-qwen-template", action="store_true")
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
            model = Reconstruction if args.stage == "reconstruction" else Formalization
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
            config = ModelConfig(
                base_url=args.base_url,
                model=args.model,
                api_key=os.getenv("PHIL_API_KEY"),
                max_tokens=args.max_tokens,
                retries=args.retries,
                timeout=args.timeout,
                structured=not args.no_structured,
                qwen_nonthinking=not args.no_qwen_template,
            )
            artifact, trace = run(args.input.read_text(), ChatClient(config))
            print(json.dumps(save(args.out, artifact, trace), indent=2))
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
