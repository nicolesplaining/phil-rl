"""Two model stages followed by deterministic diagnostics on the frozen result."""

from datetime import UTC, datetime

from phil_rl.client import ChatClient, GenerationError
from phil_rl.logic import validate_formalization
from phil_rl.normalize import ground_abstraction
from phil_rl.policy import POLICY_VERSION, explicit_only, normalized_formalization
from phil_rl.prompts import FORMALIZE, PROMPT_VERSION, RECONSTRUCT, RECONSTRUCT_UNITS
from phil_rl.schema import Artifact, Formalization, Reconstruction, fingerprint
from phil_rl.source import GroundedReconstruction, source_units
from phil_rl.verify import check


class PipelineError(GenerationError):
    def __init__(self, error: GenerationError, trace: dict):
        super().__init__(str(error), error.attempts)
        self.trace = trace


def run(
    source: str, client: ChatClient, *, legacy_quotes: bool = False
) -> tuple[Artifact | None, dict]:
    if not source.strip() or len(source) > 20000:
        raise ValueError("Provide a nonempty passage of at most 20,000 characters.")
    started = datetime.now(UTC).isoformat()
    units = source_units(source)
    reconstruction_prompt = RECONSTRUCT if legacy_quotes else RECONSTRUCT_UNITS
    trace = {
        "source": source,
        "source_sha256": fingerprint(source),
        "started_at": started,
        "prompt_version": PROMPT_VERSION,
        "policy_version": POLICY_VERSION,
        "schema_sha256": {
            "reconstruction": fingerprint(
                (Reconstruction if legacy_quotes else GroundedReconstruction).model_json_schema()
            ),
            "formalization": fingerprint(Formalization.model_json_schema()),
        },
        "prompt_sha256": {
            "reconstruction": fingerprint(reconstruction_prompt),
            "formalization": fingerprint(FORMALIZE),
        },
        "model_config": client.config.public(),
        "provenance": "llm_generated",
        "evidence_mode": "legacy_quotes" if legacy_quotes else "source_units",
        "reconstruction_attempts": [],
        "formalization_attempts": [],
    }

    def generate(stage, *args, **kwargs):
        try:
            result, attempts = client.generate(*args, **kwargs)
        except GenerationError as error:
            trace[stage + "_attempts"] = error.attempts
            trace.update(
                outcome="generation_failed",
                failed_stage=stage,
                finished_at=datetime.now(UTC).isoformat(),
                error=str(error),
            )
            raise PipelineError(error, trace) from None
        trace[stage + "_attempts"] = attempts
        return result, attempts

    if legacy_quotes:
        reconstruction, reconstruction_attempts = generate(
            "reconstruction",
            Reconstruction,
            reconstruction_prompt,
            {"source": source},
            validate=lambda result: result.validate_source(source),
        )
    else:

        def validate_grounded(result):
            if result.status == "argument":
                explicit_only(result.materialize(source, units))

        grounded, reconstruction_attempts = generate(
            "reconstruction",
            GroundedReconstruction,
            reconstruction_prompt,
            {"source_units": [unit.model_dump() for unit in units]},
            validate=validate_grounded,
        )
        if grounded.status == "no_argument":
            return None, {
                **trace,
                "outcome": "no_argument",
                "reason": grounded.reason,
                "source": source,
                "source_sha256": fingerprint(source),
                "started_at": started,
                "finished_at": datetime.now(UTC).isoformat(),
                "prompt_version": PROMPT_VERSION,
                "provenance": "llm_generated",
                "model_config": client.config.public(),
                "reconstruction_attempts": reconstruction_attempts,
                "formalization_attempts": [],
            }
        reconstruction = grounded.materialize(source, units)
    reconstruction_hash = fingerprint(reconstruction)
    trace["frozen_reconstruction"] = reconstruction.model_dump(mode="json")
    trace["reconstruction_sha256"] = reconstruction_hash
    formalization, formalization_attempts = generate(
        "formalization",
        Formalization,
        FORMALIZE,
        {"source": source, "frozen_reconstruction": reconstruction.model_dump(mode="json")},
        validate=lambda result: (
            validate_formalization if legacy_quotes else normalized_formalization
        )(reconstruction, result),
    )
    if fingerprint(reconstruction) != reconstruction_hash:
        raise ValueError("Reconstruction changed during formalization.")
    if not legacy_quotes:
        formalization, projection = ground_abstraction(formalization)
        trace["normalization"] = projection
    artifact = Artifact.create(source, reconstruction, formalization)
    trace = {
        **trace,
        "started_at": started,
        "finished_at": datetime.now(UTC).isoformat(),
        "prompt_version": PROMPT_VERSION,
        "prompt_sha256": {
            "reconstruction": fingerprint(reconstruction_prompt),
            "formalization": fingerprint(FORMALIZE),
        },
        "model_config": client.config.public(),
        "provenance": "llm_generated",
        "evidence_mode": "legacy_quotes" if legacy_quotes else "source_units",
        "reconstruction_attempts": reconstruction_attempts,
        "formalization_attempts": formalization_attempts,
        "source_spans": {
            c.id: c.evidence.locate(source) for c in reconstruction.claims if c.evidence
        },
        "explicit_check": check(artifact),
        "with_proposed_implicit_check": check(artifact, include_implicit=True),
    }
    return artifact, trace
