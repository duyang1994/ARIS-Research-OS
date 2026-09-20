"""ARIS Research OS v0.2 governance primitives.

This module is the executable heart of the v0.2 architecture upgrade.  It
implements the gates, state vocabulary, failure taxonomy, and reproducibility
levels described in the v0.2 specification.  It is intentionally dependency
free (standard library only) so that the same rules run in the repository, in
the CLI, and inside acceptance tests.

Nothing in this module writes to scientific project data.  It only reasons
about identity, provenance, freeze state, and destructive-operation intent.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence


# ---------------------------------------------------------------------------
# State vocabulary (v0.2)
# ---------------------------------------------------------------------------

OPEN = "OPEN"
PROVISIONAL = "PROVISIONAL"
AUDITED = "AUDITED"
ACCEPTED = "ACCEPTED"
FROZEN = "FROZEN"
SUPERSEDED = "SUPERSEDED"
FAILED_RETAINED = "FAILED_RETAINED"

RESEARCH_STATES = (
    OPEN,
    PROVISIONAL,
    AUDITED,
    ACCEPTED,
    FROZEN,
    SUPERSEDED,
    FAILED_RETAINED,
)

# Only these states may support downstream authoritative work.
AUTHORITATIVE_STATES = {ACCEPTED, FROZEN}

# Ephemeral sources whose outputs are PROVISIONAL by policy (v0.2 sections
# 14 and 15).
EPHEMERAL_SOURCES = (
    "stdin_helper",
    "temporary_notebook",
    "unsaved_interactive_command",
    "temporary_script",
    "shell_session",
    "interactive_console",
)


def ephemeral_result_state(source_kind: str) -> str:
    """Return the result state for a source; ephemeral sources are PROVISIONAL."""
    normalized = str(source_kind).strip().lower().replace(" ", "_")
    if normalized in EPHEMERAL_SOURCES:
        return PROVISIONAL
    return OPEN


# ---------------------------------------------------------------------------
# Reproducibility levels
# ---------------------------------------------------------------------------

REPRODUCIBILITY_LEVELS = {
    "R0": "RESULT_ONLY",
    "R1": "CODE_PRESERVED",
    "R2": "PARAMETER_COMPLETE",
    "R3": "EXECUTABLE_FREEZE",
    "R4": "CLEAN_ENVIRONMENT_REPRODUCED",
    "R5": "EXTERNALIZATION_VERIFIED",
}

MIN_LEVEL_CROSS_DATABASE_EXTERNAL_VALIDATION = "R5"


# ---------------------------------------------------------------------------
# Failure / change classification (v0.2 section 21)
# ---------------------------------------------------------------------------

SCIENTIFIC_REDESIGN = "SCIENTIFIC_REDESIGN"
REPRODUCIBILITY_GAP = "REPRODUCIBILITY_GAP"
INFRASTRUCTURE_FAILURE = "INFRASTRUCTURE_FAILURE"
DATA_AVAILABILITY_LIMITATION = "DATA_AVAILABILITY_LIMITATION"
IMPLEMENTATION_BUG = "IMPLEMENTATION_BUG"
PROVENANCE_FAILURE = "PROVENANCE_FAILURE"

FAILURE_CLASSES = (
    SCIENTIFIC_REDESIGN,
    REPRODUCIBILITY_GAP,
    INFRASTRUCTURE_FAILURE,
    DATA_AVAILABILITY_LIMITATION,
    IMPLEMENTATION_BUG,
    PROVENANCE_FAILURE,
)

# v0.2 section 9: any of these acceptance markers triggers an immediate freeze.
FREEZE_ON_ACCEPT_MARKERS = ("ACCEPT", "PRIMARY", "FINAL", "FROZEN")

# v0.2 section 20: changes to these fields require human approval, a new
# decision ID, and a new freeze ID.
MAJOR_REDESIGN_FIELDS = (
    "cohort",
    "analysis_unit",
    "anchor",
    "window",
    "feature_space",
    "endpoint",
    "external_validation_strategy",
    "primary_modelling_strategy",
)


def is_major_redesign(change_fields: Sequence[str]) -> bool:
    """Return True if any changed field requires the major-redesign gate."""
    requested = {str(f).strip().lower() for f in change_fields}
    return bool(requested & set(MAJOR_REDESIGN_FIELDS))


def should_freeze_on_accept(marker: str) -> bool:
    """Return True when a human decision marker requires freeze-on-accept."""
    return str(marker).strip().upper() in FREEZE_ON_ACCEPT_MARKERS


# ---------------------------------------------------------------------------
# Gate results
# ---------------------------------------------------------------------------

GATE_PASS = "PASS"
GATE_FAIL = "FAIL"
GATE_WAITING = "WAITING_FOR_HUMAN_REVIEW"


# ---------------------------------------------------------------------------
# Frozen Executable State component list (v0.2 section 10)
# ---------------------------------------------------------------------------

FROZEN_EXECUTABLE_STATE_COMPONENTS = (
    "design_state",
    "cohort_definition",
    "input_contract",
    "variable_order",
    "units",
    "missingness_rules",
    "cleaning_rules",
    "scalar_parameters",
    "seeds",
    "thresholds",
    "fitted_objects",
    "runtime_derived_objects",
    "reference_population_state",
    "model_checkpoints",
    "normalization_constants",
    "calibration_objects",
    "exact_code",
    "git_sha_or_file_hashes",
    "runtime_environment",
    "output_contract",
    "smoke_test_input",
    "expected_smoke_test_output",
    "integrity_manifest",
)


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


def _to_bool(value: Any) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        v = value.strip().lower()
        if v in {"true", "yes", "y", "1"}:
            return True
        if v in {"false", "no", "n", "0"}:
            return False
    return None


def _scalar(value: str) -> Any:
    """Convert a single YAML scalar string to a python scalar."""
    value = value.strip()
    if value == "":
        return ""
    b = _to_bool(value)
    if b is not None:
        return b
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    if value.lower() in {"null", "none", "~"}:
        return None
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def parse_simple_yaml(text: str) -> Dict[str, Any]:
    """Parse the deliberately small YAML subset used by ARIS governance files.

    Supported constructs are sufficient for PROJECT_IDENTITY.yaml,
    CONSTRAINTS.yaml, and PROJECT_NAMESPACE.yaml:

    * ``key: value`` scalars (strings, booleans, numbers, quoted strings)
    * ``key:`` followed by indented ``- item`` list entries
    * blank lines and ``#`` comments
    """
    result: Dict[str, Any] = {}
    current_list: Optional[str] = None
    for raw in text.splitlines():
        line = raw.rstrip("\r\n")
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line.startswith((" ", "\t")) and stripped.startswith("- "):
            item = stripped[2:].strip()
            if current_list is not None:
                result.setdefault(current_list, []).append(item)
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if not key:
                continue
            if value == "":
                current_list = key
                result.setdefault(key, [])
            else:
                current_list = None
                result[key] = _scalar(value)
    return result


def normalize_root(value: Any) -> str:
    """Normalize a filesystem root string for comparison."""
    if value is None:
        return ""
    return str(value).replace("/", "\\").rstrip("\\").lower()


def string_contains_any(text: str, needles: Sequence[str]) -> List[str]:
    """Return the lowercase needles found in ``text``."""
    lower = str(text).lower()
    found: List[str] = []
    for needle in needles:
        if needle and str(needle).lower() in lower:
            found.append(str(needle))
    return found


# ---------------------------------------------------------------------------
# Result envelope
# ---------------------------------------------------------------------------


@dataclass
class GateResult:
    gate: str
    result: str = GATE_WAITING
    checks: List[Dict[str, Any]] = field(default_factory=list)
    reasons: List[str] = field(default_factory=list)

    def add(self, name: str, passed: bool, detail: str = "") -> None:
        self.checks.append(
            {
                "check": name,
                "result": GATE_PASS if passed else GATE_FAIL,
                "detail": detail,
            }
        )
        if not passed:
            self.reasons.append(f"{name}: {detail}" if detail else name)

    def finalize(self, allow_waiting: bool = True) -> "GateResult":
        if self.reasons:
            self.result = GATE_FAIL
        elif allow_waiting and any(
            c["result"] == GATE_WAITING for c in self.checks
        ):
            self.result = GATE_WAITING
        else:
            self.result = GATE_PASS
        return self

    def as_dict(self) -> Dict[str, Any]:
        return {
            "gate": self.gate,
            "result": self.result,
            "checks": self.checks,
            "reasons": self.reasons,
        }


# ---------------------------------------------------------------------------
# GATE_PROJECT_IDENTITY (v0.2 sections 2, 3)
# ---------------------------------------------------------------------------


def project_identity_gate(
    identity: Dict[str, Any],
    requested: Optional[Dict[str, Any]] = None,
    *,
    task_paths: Optional[Sequence[str]] = None,
    read_sources: Optional[Sequence[str]] = None,
    write_target: Optional[str] = None,
) -> GateResult:
    """Run the mandatory first gate before any substantive execution."""
    requested = requested or {}
    gate = GateResult(gate="GATE_PROJECT_IDENTITY")
    task_paths = list(task_paths or [])
    read_sources = list(read_sources or [])

    required_fields = [
        "project_id",
        "canonical_root",
        "scientific_question",
        "primary_analysis_unit",
    ]
    missing = [f for f in required_fields if not identity.get(f)]
    if missing:
        gate.add(
            "identity_complete",
            False,
            f"missing required field(s): {', '.join(missing)}",
        )
        gate.finalize()
        return gate
    gate.add("identity_complete", True)

    project_id = str(identity.get("project_id", ""))
    requested_id = str(requested.get("project_id", ""))
    gate.add(
        "project_id_matches_requested_task",
        not requested_id or requested_id == project_id,
        f"identity={project_id!r} requested={requested_id!r}",
    )

    canonical_root = normalize_root(identity.get("canonical_root"))
    requested_root = normalize_root(requested.get("canonical_root", canonical_root))
    gate.add(
        "canonical_root_matches",
        requested_root == canonical_root,
        f"identity={canonical_root!r} requested={requested_root!r}",
    )

    forbidden_roots = [
        normalize_root(r) for r in (identity.get("forbidden_project_roots") or [])
    ]
    combined_paths = " ".join(task_paths + read_sources + [write_target or ""])
    referenced_forbidden = [
        r
        for r in forbidden_roots
        if r and r in normalize_root(combined_paths).lower()
    ]
    gate.add(
        "no_forbidden_project_root_referenced",
        not referenced_forbidden,
        f"forbidden roots referenced: {referenced_forbidden}"
        if referenced_forbidden
        else "no forbidden root referenced",
    )

    foreign_signatures = [str(s) for s in (identity.get("foreign_project_signatures") or [])]
    foreign_hits = string_contains_any(
        " ".join(task_paths + read_sources), foreign_signatures
    )
    gate.add(
        "no_foreign_project_signature",
        not foreign_hits,
        f"foreign signatures found: {foreign_hits}"
        if foreign_hits
        else "no foreign signature found",
    )

    write_target_ok = True
    if write_target:
        write_target_ok = normalize_root(write_target).startswith(canonical_root)
    gate.add(
        "write_target_belongs_to_current_project",
        write_target_ok,
        f"write_target={write_target!r} canonical_root={canonical_root!r}",
    )

    external_inputs = [
        str(s) for s in (identity.get("approved_external_sources") or [])
    ]
    input_ok = True
    bad_inputs: List[str] = []
    for source in read_sources:
        s = str(source)
        if normalize_root(s).startswith(canonical_root):
            continue
        if any(normalize_root(x) in normalize_root(s) for x in external_inputs if x):
            continue
        input_ok = False
        bad_inputs.append(s)
    gate.add(
        "input_files_belong_to_current_project",
        input_ok,
        f"unapproved external inputs: {bad_inputs}" if bad_inputs else "inputs in scope",
    )

    return gate.finalize()


# ---------------------------------------------------------------------------
# GATE_EXECUTABLE_FREEZE (v0.2 sections 10, 50)
# ---------------------------------------------------------------------------


def frozen_executable_state_gate(
    manifest: Dict[str, Any],
    *,
    required: Sequence[str] = FROZEN_EXECUTABLE_STATE_COMPONENTS,
) -> GateResult:
    """Verify that a freeze contains the complete executable state."""
    gate = GateResult(gate="GATE_EXECUTABLE_FREEZE")
    present = set(manifest.keys())
    missing = [c for c in required if c not in present]
    gate.add("all_required_components_present", not missing, f"missing={missing}")
    for key, value in manifest.items():
        if key in required and value in (None, "", [], {}):
            gate.add(f"component_nonempty:{key}", False, "component is empty")
    return gate.finalize(allow_waiting=False)


# ---------------------------------------------------------------------------
# GATE_EXTERNAL_REPLAY (v0.2 section 25)
# ---------------------------------------------------------------------------


def external_replay_gate(
    *,
    generic_wrapper_exists: bool,
    reference_replay_pass: bool,
    prior_freeze_id: Optional[str],
    target_database: Optional[str],
) -> GateResult:
    """External validation may begin only after replay of an accepted dataset."""
    gate = GateResult(gate="GATE_EXTERNAL_REPLAY")
    gate.add("generic_wrapper_exists", generic_wrapper_exists)
    gate.add("reference_replay_pass", reference_replay_pass)
    gate.add("prior_freeze_exists", bool(prior_freeze_id))
    gate.add("target_database_declared", bool(target_database))
    return gate.finalize(allow_waiting=False)


# ---------------------------------------------------------------------------
# GATE_DESTRUCTIVE_OPERATION (v0.2 section 36)
# ---------------------------------------------------------------------------


@dataclass
class DestructivePlan:
    operation: str
    targets: List[str]
    authorized: bool = False
    human_decision_id: Optional[str] = None


def destructive_operation_gate(plan: DestructivePlan) -> GateResult:
    """Produce an explicit target list; require human authorization."""
    gate = GateResult(gate="GATE_DESTRUCTIVE_OPERATION")
    gate.add("targets_enumerated", bool(plan.targets), f"targets={plan.targets}")
    gate.add(
        "human_authorization_present",
        plan.authorized and bool(plan.human_decision_id),
        f"authorized={plan.authorized} decision_id={plan.human_decision_id}",
    )
    return gate.finalize(allow_waiting=False)


# ---------------------------------------------------------------------------
# Execution preflight (v0.2 section 35)
# ---------------------------------------------------------------------------


def execution_preflight(
    identity: Dict[str, Any],
    task: Dict[str, Any],
) -> GateResult:
    """Return PREFLIGHT_PASS only after every pre-execution check passes."""
    gate = GateResult(gate="EXECUTION_PREFLIGHT")
    requested = {
        "project_id": task.get("project_id"),
        "canonical_root": task.get("canonical_root"),
    }
    identity_gate = project_identity_gate(
        identity,
        requested,
        task_paths=[task.get("write_target", "")],
        read_sources=task.get("read_sources", []) or [],
        write_target=task.get("write_target"),
    )
    gate.add(
        "project_identity_passes",
        identity_gate.result == GATE_PASS,
        identity_gate.result,
    )
    gate.add("write_target_declared", bool(task.get("write_target")))
    gate.add(
        "upstream_freeze_declared",
        bool(task.get("upstream_freeze_id")),
        f"upstream_freeze_id={task.get('upstream_freeze_id')!r}",
    )
    gate.add("destructive_operations_declared", "destructive_operations" in task)
    gate.add(
        "no_destructive_operations",
        not bool(task.get("destructive_operations")),
        f"destructive_operations={task.get('destructive_operations')!r}",
    )
    gate.add("expected_output_declared", bool(task.get("expected_output")))
    return gate.finalize(allow_waiting=False)


# ---------------------------------------------------------------------------
# Failure classification (v0.2 section 21)
# ---------------------------------------------------------------------------


FAILURE_KEYWORDS = {
    PROVENANCE_FAILURE: {"wrong project root", "wrong root", "cross-project", "foreign root"},
    REPRODUCIBILITY_GAP: {"missing checkpoint", "missing artifact", "missing file", "missing object"},
    INFRASTRUCTURE_FAILURE: {"torch mismatch", "environment", "cuda", "version mismatch", "dependency"},
    DATA_AVAILABILITY_LIMITATION: {"missing sodium", "missing variable", "not available", "external database"},
    IMPLEMENTATION_BUG: {"bug", "typo", "off-by-one", "incorrect formula"},
    SCIENTIFIC_REDESIGN: {
        "first-stay to all-stays",
        "cohort change",
        "analysis unit",
        "endpoint change",
        "redesign",
    },
}


def classify_failure(description: str) -> str:
    """Classify a change/failure description into an explicit v0.2 class."""
    text = str(description).lower()
    for class_name, keywords in FAILURE_KEYWORDS.items():
        if any(k in text for k in keywords):
            return class_name
    return PROVENANCE_FAILURE


# ---------------------------------------------------------------------------
# Result review order (v0.2 section 16)
# ---------------------------------------------------------------------------

RESULT_REVIEW_ORDER = (
    "PROJECT_IDENTITY",
    "SCIENTIFIC_DESIGN",
    "INPUT_LINEAGE",
    "FREEZE_PROVENANCE",
    "IMPLEMENTATION",
    "RESULT",
    "REPRODUCIBILITY",
    "INTERPRETATION",
)

RESULT_REVIEW_HEADER_FIELDS = (
    "PROJECT_IDENTITY",
    "SCIENTIFIC_FINGERPRINT",
    "INPUT_LINEAGE",
    "FREEZE_STATE",
    "IMPLEMENTATION",
    "RESULT_VALIDITY",
    "REPRODUCIBILITY",
    "HUMAN_DECISION_REQUIRED",
)


def result_review_gate(review: Dict[str, Any]) -> GateResult:
    """Enforce audit-before-interpretation ordering."""
    gate = GateResult(gate="GATE_RESULT_REVIEW")
    ordered = [str(review.get(f, "")).upper() for f in RESULT_REVIEW_ORDER]
    first_interpretation = (
        ordered.index("INTERPRETATION") if "INTERPRETATION" in ordered else len(ordered)
    )
    pre_interpretation = ordered[:first_interpretation]
    gate.add(
        "audit_fields_precede_interpretation",
        first_interpretation == len(RESULT_REVIEW_ORDER) - 1,
        f"order={ordered}",
    )
    gate.add(
        "project_identity_evaluated_first",
        bool(pre_interpretation) and pre_interpretation[0] == "PROJECT_IDENTITY",
    )
    return gate.finalize(allow_waiting=False)


# ---------------------------------------------------------------------------
# Stop conditions (v0.2 section 43)
# ---------------------------------------------------------------------------

STOP_CONDITIONS = (
    "project identity mismatch",
    "canonical root mismatch",
    "foreign project contamination",
    "scientific definition conflict",
    "missing authoritative freeze",
    "unexplained hash mismatch",
    "missing fitted object",
    "unresolved major redesign",
    "destructive operation without authorization",
    "unexpected cohort change",
    "unexpected analysis-unit change",
)


def is_stop_condition(reason: str) -> bool:
    reason_lower = reason.lower()
    return any(condition in reason_lower for condition in STOP_CONDITIONS)
