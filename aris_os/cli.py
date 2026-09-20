import argparse
import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from .bootstrap import bootstrap_project_v02, read_identity
from .governance import (
    DestructivePlan,
    MIN_LEVEL_CROSS_DATABASE_EXTERNAL_VALIDATION,
    REPRODUCIBILITY_LEVELS,
    classify_failure,
    destructive_operation_gate,
    execution_preflight,
    external_replay_gate,
    frozen_executable_state_gate,
    parse_simple_yaml,
    project_identity_gate,
)
from .models import Event
from .rules import requires_human_review
from .store import ResearchStore

TEMPLATES = [
    "RESEARCH_PLAN.md",
    "DECISION_REGISTER.md",
    "GATE_REGISTER.md",
    "THREAD_STATUS.md",
    "RESULT_REGISTRY.md",
    "CLAIM_REGISTRY.md",
    "FIGURE_TABLE_REGISTRY.md",
    "LITERATURE_REGISTRY.md",
    "MANUSCRIPT_STATE.md",
    "RESEARCH_INBOX.md",
    "WORKFLOW_LESSONS.md",
    "PROJECT_IDENTITY.yaml",
    "PROJECT_STATUS.md",
    "MASTER_INDEX.md",
    "CONSTRAINTS.yaml",
    "PROJECT_NAMESPACE.yaml",
    "HUMAN_PREFLIGHT_HEADER.md",
    "HUMAN_DECISION_PACKET.md",
    "RESULT_REVIEW_HEADER.md",
    "INCIDENT_REPORT.md",
    "OPEN_QUESTIONS.md",
    "FROZEN_PARAMETER_REGISTRY.csv",
    "FROZEN_ARTIFACT_REGISTRY.csv",
    "FROZEN_EXECUTABLE_STATE_MANIFEST.yaml",
    "RESULTS_LEDGER.csv",
    "CLAIM_LEDGER.csv",
]


def package_root():
    return Path(__file__).resolve().parents[1]


def init_project(root, name):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    (root / ".aris").mkdir(exist_ok=True)
    (root / "test").mkdir(exist_ok=True)
    (root / "manuscript").mkdir(exist_ok=True)
    for t in TEMPLATES:
        src = package_root() / "templates" / t
        dst = root / t
        if not dst.exists():
            shutil.copy2(src, dst)
    store = ResearchStore(root)
    print(f"Initialized ARIS project: {name}")
    print(f"State DB: {store.db_path}")


def status(root):
    store = ResearchStore(root)
    for table in ["threads", "gates", "decisions", "results", "claims", "events"]:
        print(f"\n[{table}]")
        for row in store.rows(table):
            print(row)


def add_event(root, event_type, source, summary):
    store = ResearchStore(root)
    ev = Event(
        event_id=f"EV-{uuid.uuid4().hex[:8]}",
        event_type=event_type,
        source=source,
        summary=summary,
        requires_human_review=requires_human_review(event_type),
    )
    store.insert_dataclass("events", ev)
    print(ev)


def daily_brief(root):
    store = ResearchStore(root)
    events = store.rows("events")
    decisions = store.rows("decisions")
    results = store.rows("results")
    print("# PI DAILY BRIEF")
    print(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    print(f"\nNew events: {len(events)}")
    print(f"Decisions: {len(decisions)}")
    print(f"Results: {len(results)}")
    action = [e for e in events if e.get("requires_human_review")]
    print(f"Action required: {len(action)}")
    for e in action[-10:]:
        print(f"- {e['event_id']}: {e['summary']}")


def cmd_bootstrap(root):
    report = bootstrap_project_v02(root)
    print(json.dumps(report, indent=2, ensure_ascii=False))


def cmd_identity_gate(args):
    identity = read_identity(args.root)
    requested = {
        "project_id": args.project_id,
        "canonical_root": args.canonical_root,
    }
    gate = project_identity_gate(
        identity,
        requested,
        read_sources=list(args.read_source or []),
        write_target=args.write_target,
    )
    print(json.dumps(gate.as_dict(), indent=2, ensure_ascii=False))


def cmd_preflight(args):
    identity = read_identity(args.root)
    task = {
        "project_id": args.project_id,
        "canonical_root": args.canonical_root,
        "write_target": args.write_target,
        "read_sources": list(args.read_source or []),
        "upstream_freeze_id": args.upstream_freeze_id,
        "expected_output": args.expected_output,
        "destructive_operations": [],
    }
    gate = execution_preflight(identity, task)
    print(json.dumps(gate.as_dict(), indent=2, ensure_ascii=False))


def cmd_freeze_check(args):
    text = Path(args.manifest).read_text(encoding="utf-8")
    manifest = parse_simple_yaml(text)
    gate = frozen_executable_state_gate(manifest)
    print(json.dumps(gate.as_dict(), indent=2, ensure_ascii=False))


def cmd_external_replay(args):
    gate = external_replay_gate(
        generic_wrapper_exists=args.generic_wrapper,
        reference_replay_pass=args.reference_replay_pass,
        prior_freeze_id=args.prior_freeze_id,
        target_database=args.target_database,
    )
    print(json.dumps(gate.as_dict(), indent=2, ensure_ascii=False))


def cmd_destructive(args):
    plan = DestructivePlan(
        operation=args.operation,
        targets=list(args.target),
        authorized=args.authorized,
        human_decision_id=args.decision_id,
    )
    gate = destructive_operation_gate(plan)
    print(json.dumps(gate.as_dict(), indent=2, ensure_ascii=False))


def cmd_classify(args):
    print(classify_failure(args.description))


def cmd_reproducibility(args):
    level = args.level.upper()
    print(REPRODUCIBILITY_LEVELS.get(level, "UNKNOWN_LEVEL"))
    if level >= "R5":
        print(f"Minimum for cross-database external validation: {MIN_LEVEL_CROSS_DATABASE_EXTERNAL_VALIDATION}")


def main():
    p = argparse.ArgumentParser(
        prog="aris",
        description="ARIS Research OS v0.2 governance control plane.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("init-project", help="Initialize a new ARIS project.")
    a.add_argument("--root", required=True, help="Project root directory.")
    a.add_argument("--name", required=True, help="Human-readable project name.")

    s = sub.add_parser("status", help="Show state-store tables for a project.")
    s.add_argument("--root", required=True, help="Project root directory.")

    e = sub.add_parser("add-event", help="Record a research event.")
    e.add_argument("--root", required=True, help="Project root directory.")
    e.add_argument("--type", required=True, help="Event type.")
    e.add_argument("--source", required=True, help="Agent or tool that emitted the event.")
    e.add_argument("--summary", required=True, help="One-line event summary.")

    d = sub.add_parser("daily-brief", help="Print a compact PI daily brief.")
    d.add_argument("--root", required=True, help="Project root directory.")

    b = sub.add_parser(
        "bootstrap-project-v02",
        help="Add v0.2 governance scaffolding to an existing project.",
    )
    b.add_argument("--root", required=True, help="Project root directory.")

    ig = sub.add_parser("gate-identity", help="Run GATE_PROJECT_IDENTITY.")
    ig.add_argument("--root", required=True, help="Project root containing PROJECT_IDENTITY.yaml.")
    ig.add_argument("--project-id", help="Requested project ID.")
    ig.add_argument("--canonical-root", help="Requested canonical root.")
    ig.add_argument("--write-target", help="Requested write target.")
    ig.add_argument("--read-source", action="append", help="Requested read source (repeatable).")

    pf = sub.add_parser("preflight", help="Run execution preflight checks.")
    pf.add_argument("--root", required=True, help="Project root containing PROJECT_IDENTITY.yaml.")
    pf.add_argument("--project-id", help="Requested project ID.")
    pf.add_argument("--canonical-root", help="Requested canonical root.")
    pf.add_argument("--write-target", required=True, help="Requested write target.")
    pf.add_argument("--read-source", action="append", help="Requested read source (repeatable).")
    pf.add_argument("--upstream-freeze-id", required=True, help="Upstream freeze ID.")
    pf.add_argument("--expected-output", required=True, help="Expected output location.")

    fc = sub.add_parser("freeze-check", help="Verify a frozen executable state manifest.")
    fc.add_argument("--manifest", required=True, help="Path to the freeze manifest YAML.")

    er = sub.add_parser("external-replay-gate", help="Run GATE_EXTERNAL_REPLAY.")
    er.add_argument("--generic-wrapper", action="store_true", help="Generic wrapper exists.")
    er.add_argument("--reference-replay-pass", action="store_true", help="Reference replay passed.")
    er.add_argument("--prior-freeze-id", help="Prior freeze ID.")
    er.add_argument("--target-database", help="Target external database name.")

    do = sub.add_parser("destructive-gate", help="Run GATE_DESTRUCTIVE_OPERATION.")
    do.add_argument("--operation", required=True, help="Destructive operation name.")
    do.add_argument("--target", action="append", required=True, help="Exact target path (repeatable).")
    do.add_argument("--authorized", action="store_true", help="Human authorization present.")
    do.add_argument("--decision-id", help="Human decision ID.")

    cf = sub.add_parser("classify-failure", help="Classify a change or failure.")
    cf.add_argument("--description", required=True, help="Failure/change description.")

    rl = sub.add_parser("reproducibility", help="Resolve a reproducibility level.")
    rl.add_argument("--level", required=True, help="Level such as R0 through R5.")

    args = p.parse_args()
    if args.cmd == "init-project":
        init_project(args.root, args.name)
    elif args.cmd == "status":
        status(args.root)
    elif args.cmd == "add-event":
        add_event(args.root, args.type, args.source, args.summary)
    elif args.cmd == "daily-brief":
        daily_brief(args.root)
    elif args.cmd == "bootstrap-project-v02":
        cmd_bootstrap(args.root)
    elif args.cmd == "gate-identity":
        cmd_identity_gate(args)
    elif args.cmd == "preflight":
        cmd_preflight(args)
    elif args.cmd == "freeze-check":
        cmd_freeze_check(args)
    elif args.cmd == "external-replay-gate":
        cmd_external_replay(args)
    elif args.cmd == "destructive-gate":
        cmd_destructive(args)
    elif args.cmd == "classify-failure":
        cmd_classify(args)
    elif args.cmd == "reproducibility":
        cmd_reproducibility(args)


if __name__ == "__main__":
    main()
