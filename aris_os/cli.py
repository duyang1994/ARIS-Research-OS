import argparse
from pathlib import Path
from datetime import datetime
import shutil
import uuid

from .store import ResearchStore
from .models import Event
from .rules import requires_human_review

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

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("init-project")
    a.add_argument("--root", required=True)
    a.add_argument("--name", required=True)

    s = sub.add_parser("status")
    s.add_argument("--root", required=True)

    e = sub.add_parser("add-event")
    e.add_argument("--root", required=True)
    e.add_argument("--type", required=True)
    e.add_argument("--source", required=True)
    e.add_argument("--summary", required=True)

    d = sub.add_parser("daily-brief")
    d.add_argument("--root", required=True)

    args = p.parse_args()
    if args.cmd == "init-project":
        init_project(args.root, args.name)
    elif args.cmd == "status":
        status(args.root)
    elif args.cmd == "add-event":
        add_event(args.root, args.type, args.source, args.summary)
    elif args.cmd == "daily-brief":
        daily_brief(args.root)

if __name__ == "__main__":
    main()
