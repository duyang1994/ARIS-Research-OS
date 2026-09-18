from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional

def now_iso():
    return datetime.now(timezone.utc).isoformat()

@dataclass
class Event:
    event_id: str
    event_type: str
    source: str
    summary: str
    severity: str = "INFO"
    thread_id: Optional[str] = None
    result_id: Optional[str] = None
    requires_human_review: bool = False
    created_at: str = field(default_factory=now_iso)

@dataclass
class Decision:
    decision_id: str
    topic: str
    decision: str
    status: str = "ACTIVE"
    evidence: str = ""
    major_redesign: bool = False
    created_at: str = field(default_factory=now_iso)

@dataclass
class Result:
    result_id: str
    experiment_id: str
    question: str
    summary: str
    status: str = "EXPLORATORY"
    supersedes: Optional[str] = None
    decision_id: Optional[str] = None
    created_at: str = field(default_factory=now_iso)

@dataclass
class Claim:
    claim_id: str
    text: str
    status: str = "CANDIDATE"
    evidence_ids: str = ""
    manuscript_locations: str = ""
    created_at: str = field(default_factory=now_iso)

@dataclass
class ThreadState:
    thread_id: str
    name: str
    state: str = "PLANNED"
    dependency: str = ""
    gate_name: str = ""          # P-1: matches the SQLite column name in store.SCHEMA
    next_action: str = ""
    human_review_required: bool = False
    updated_at: str = field(default_factory=now_iso)
