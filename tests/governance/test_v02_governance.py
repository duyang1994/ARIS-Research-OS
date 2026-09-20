"""Acceptance tests for ARIS Research OS v0.2 governance."""

import pytest

from aris_os.governance import (
    DestructivePlan,
    FROZEN_EXECUTABLE_STATE_COMPONENTS,
    PROVISIONAL,
    GATE_FAIL,
    GATE_PASS,
    classify_failure,
    destructive_operation_gate,
    ephemeral_result_state,
    external_replay_gate,
    frozen_executable_state_gate,
    project_identity_gate,
)


def _project_a_identity():
    return {
        "project_id": "PROJECT-A",
        "project_title": "Project A",
        "canonical_root": r"D:\ProjectA",
        "scientific_question": "A-specific question",
        "primary_analysis_unit": "first admission",
        "forbidden_project_roots": [r"D:\ProjectB"],
        "foreign_project_signatures": ["project-b-signature"],
    }


def test_cross_project_identity_fails():
    identity = _project_a_identity()
    gate = project_identity_gate(
        identity,
        {"project_id": "PROJECT-B", "canonical_root": r"D:\ProjectB"},
        write_target=r"D:\ProjectB\analysis\stage01",
    )
    assert gate.result == GATE_FAIL
    assert gate.gate == "GATE_PROJECT_IDENTITY"


def test_matching_identity_passes():
    identity = _project_a_identity()
    gate = project_identity_gate(
        identity,
        {"project_id": "PROJECT-A", "canonical_root": r"D:\ProjectA"},
        write_target=r"D:\ProjectA\analysis\stage01",
    )
    assert gate.result == GATE_PASS


def test_accepted_result_with_unsaved_scaler_fails_freeze():
    manifest = {component: "present" for component in FROZEN_EXECUTABLE_STATE_COMPONENTS}
    # The scaler is runtime-derived and was never saved.
    manifest["runtime_derived_objects"] = ""
    manifest["fitted_objects"] = ""
    gate = frozen_executable_state_gate(manifest)
    assert gate.result == GATE_FAIL
    assert gate.gate == "GATE_EXECUTABLE_FREEZE"


def test_ephemeral_stdin_result_is_provisional():
    assert ephemeral_result_state("stdin helper") == PROVISIONAL
    assert ephemeral_result_state("temporary_notebook") == PROVISIONAL
    assert ephemeral_result_state("unsaved_interactive_command") == PROVISIONAL


def test_external_validation_without_replay_fails():
    gate = external_replay_gate(
        generic_wrapper_exists=True,
        reference_replay_pass=False,
        prior_freeze_id="FREEZE-20260101-0001",
        target_database="ExternalDatasetC",
    )
    assert gate.result == GATE_FAIL
    assert gate.gate == "GATE_EXTERNAL_REPLAY"


def test_destructive_operation_without_approval_fails():
    plan = DestructivePlan(
        operation="delete",
        targets=[r"C:\Research\ProjectAlpha\analysis\stage01"],
        authorized=False,
        human_decision_id=None,
    )
    gate = destructive_operation_gate(plan)
    assert gate.result == GATE_FAIL
    assert gate.gate == "GATE_DESTRUCTIVE_OPERATION"


def test_valid_frozen_project_passes():
    manifest = {component: "present" for component in FROZEN_EXECUTABLE_STATE_COMPONENTS}
    gate = frozen_executable_state_gate(manifest)
    assert gate.result == GATE_PASS
    assert gate.gate == "GATE_EXECUTABLE_FREEZE"


def test_failure_classification():
    assert classify_failure("wrong project root selected") == "PROVENANCE_FAILURE"
    assert classify_failure("missing checkpoint") == "REPRODUCIBILITY_GAP"
    assert classify_failure("torch mismatch in environment") == "INFRASTRUCTURE_FAILURE"
    assert classify_failure("changing first-stay to all-stays") == "SCIENTIFIC_REDESIGN"
