import pytest

from phil_rl.examples import fixtures
from phil_rl.source import GroundedReconstruction, source_units


def draft_for(artifact):
    units = source_units(artifact.source)
    data = artifact.reconstruction.model_dump()
    for claim in data["claims"]:
        evidence = claim.pop("evidence")
        if evidence is None:
            claim["evidence_ids"] = []
        else:
            claim["evidence_ids"] = [unit.id for unit in units if unit.text == evidence["quote"]][
                evidence["occurrence"] : evidence["occurrence"] + 1
            ]
    return GroundedReconstruction.model_validate(data), units


@pytest.mark.parametrize("name", list(fixtures()))
def test_materialized_evidence_matches_existing_fixtures(name):
    artifact = fixtures()[name][0]
    draft, units = draft_for(artifact)
    assert draft.materialize(artifact.source, units) == artifact.reconstruction


def test_source_units_preserve_unicode_punctuation_and_newlines():
    source = '  自由.\nP is 1.5. "Really?"  P is 1.5.\n'
    units = source_units(source)
    assert [unit.text for unit in units] == ["自由.", "P is 1.5.", '"Really?"', "P is 1.5."]
    assert all(source[u.start : u.end] == u.text for u in units)


@pytest.mark.parametrize("ids", [[], ["s999"], ["s2", "s1"], ["s1", "s3"], ["s1", "s1"]])
def test_invalid_evidence_selection_is_rejected(ids):
    artifact = fixtures()["modus_ponens"][0]
    draft, units = draft_for(artifact)
    data = draft.model_dump()
    data["claims"][0]["evidence_ids"] = ids
    with pytest.raises(ValueError):
        GroundedReconstruction.model_validate(data).materialize(artifact.source, units)


def test_adjacent_evidence_can_span_abbreviation_splits():
    artifact = fixtures()["modus_ponens"][0]
    draft, units = draft_for(artifact)
    data = draft.model_dump()
    data["claims"][0]["evidence_ids"] = ["s1", "s2"]
    result = GroundedReconstruction.model_validate(data).materialize(artifact.source, units)
    assert result.claims[0].evidence.quote == artifact.source[: units[1].end]
