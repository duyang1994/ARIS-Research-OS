import sqlite3
from pathlib import Path
from dataclasses import asdict

SCHEMA = """
CREATE TABLE IF NOT EXISTS events(
  event_id TEXT PRIMARY KEY,
  event_type TEXT,
  source TEXT,
  summary TEXT,
  severity TEXT,
  thread_id TEXT,
  result_id TEXT,
  requires_human_review INTEGER,
  created_at TEXT
);
CREATE TABLE IF NOT EXISTS decisions(
  decision_id TEXT PRIMARY KEY,
  topic TEXT,
  decision TEXT,
  status TEXT,
  evidence TEXT,
  major_redesign INTEGER,
  created_at TEXT
);
CREATE TABLE IF NOT EXISTS results(
  result_id TEXT PRIMARY KEY,
  experiment_id TEXT,
  question TEXT,
  summary TEXT,
  status TEXT,
  supersedes TEXT,
  decision_id TEXT,
  created_at TEXT
);
CREATE TABLE IF NOT EXISTS claims(
  claim_id TEXT PRIMARY KEY,
  text TEXT,
  status TEXT,
  evidence_ids TEXT,
  manuscript_locations TEXT,
  created_at TEXT
);
CREATE TABLE IF NOT EXISTS threads(
  thread_id TEXT PRIMARY KEY,
  name TEXT,
  state TEXT,
  dependency TEXT,
  gate_name TEXT,
  next_action TEXT,
  human_review_required INTEGER,
  updated_at TEXT
);
CREATE TABLE IF NOT EXISTS gates(
  gate_id TEXT PRIMARY KEY,
  status TEXT,
  conditions TEXT,
  updated_at TEXT
);
"""

class ResearchStore:
    def __init__(self, project_root):
        self.root = Path(project_root)
        self.db_path = self.root / ".aris" / "research_state.sqlite3"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def insert_dataclass(self, table, obj):
        d = asdict(obj)
        d = {k: int(v) if isinstance(v, bool) else v for k, v in d.items()}
        cols = ",".join(d.keys())
        qs = ",".join(["?"] * len(d))
        self.conn.execute(
            f"INSERT OR REPLACE INTO {table} ({cols}) VALUES ({qs})",
            tuple(d.values())
        )
        self.conn.commit()

    def rows(self, table):
        return [dict(r) for r in self.conn.execute(f"SELECT * FROM {table}").fetchall()]
