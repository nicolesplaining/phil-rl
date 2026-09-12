"""Archive generated research runs with file hashes, without overwriting results."""

import hashlib
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path


def archive_run(source: Path, destination: Path, run_commit: str):
    if destination.exists():
        raise ValueError("Archive destination already exists.")
    if not (source / "summary.json").is_file() and not (source / "trace.json").is_file():
        raise ValueError("Archive a run with summary.json or trace.json.")
    if source.is_symlink() or destination.resolve().is_relative_to(source.resolve()):
        raise ValueError("Use a real source directory and a destination outside it.")
    files = sorted(source.rglob("*"))
    if any(
        p.is_symlink() or (p.is_file() and p.suffix not in {".json", ".md", ".lean"}) for p in files
    ):
        raise ValueError("Run archives allow only JSON, Markdown and Lean files, without symlinks.")
    if "archive-manifest.json" in {p.name for p in files}:
        raise ValueError("Archive the original run, not an existing archive.")
    checksums = {
        str(p.relative_to(source)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in files
        if p.is_file()
    }
    shutil.copytree(source, destination)
    manifest = {
        "archived_at": datetime.now(UTC).isoformat(),
        "run_code_commit": run_commit,
        "sha256": checksums,
        "note": "Hashes identify saved files, not independent validation of their claims.",
    }
    (destination / "archive-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return {"files": len(checksums), "destination": str(destination)}
