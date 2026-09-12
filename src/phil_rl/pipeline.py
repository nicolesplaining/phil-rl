"""Two model stages followed by deterministic diagnostics on the frozen result."""

from datetime import UTC, datetime

from phil_rl.client import ChatClient
from phil_rl.logic import validate_formalization
from phil_rl.prompts import FORMALIZE, PROMPT_VERSION, RECONSTRUCT
from phil_rl.schema import Artifact, Formalization, Reconstruction, fingerprint
from phil_rl.verify import check


def run(source: str, client: ChatClient) -> tuple[Artifact, dict]:
    if not source.strip() or len(source) > 20000:
        raise ValueError("Provide a nonempty passage of at most 20,000 characters.")
    started = datetime.now(UTC).isoformat()
    reconstruction, reconstruction_attempts = client.generate(
        Reconstruction,
        RECONSTRUCT,
        {"source": source},
        validate=lambda result: result.validate_source(source),
    )
    reconstruction_hash = fingerprint(reconstruction)
    formalization, formalization_attempts = client.generate(
        Formalization,
        FORMALIZE,
        {"source": source, "frozen_reconstruction": reconstruction.model_dump(mode="json")},
        validate=lambda result: validate_formalization(reconstruction, result),
    )
    if fingerprint(reconstruction) != reconstruction_hash:
        raise ValueError("Reconstruction changed during formalization.")
    artifact = Artifact.create(source, reconstruction, formalization)
    trace = {
        "started_at": started,
        "finished_at": datetime.now(UTC).isoformat(),
        "prompt_version": PROMPT_VERSION,
        "prompt_sha256": {
            "reconstruction": fingerprint(RECONSTRUCT),
            "formalization": fingerprint(FORMALIZE),
        },
        "model_config": client.config.public(),
        "provenance": "llm_generated",
        "reconstruction_attempts": reconstruction_attempts,
        "formalization_attempts": formalization_attempts,
        "source_spans": {
            c.id: c.evidence.locate(source) for c in reconstruction.claims if c.evidence
        },
        "explicit_check": check(artifact),
        "with_proposed_implicit_check": check(artifact, include_implicit=True),
    }
    return artifact, trace
