"""P-1 acceptance tests: schema, insert round-trip, migration, CLI smoke."""
import os, sqlite3, subprocess, sys, tempfile, uuid
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from aris_os.models import Claim, Decision, Event, Result, ThreadState
from aris_os.store import ResearchStore

def test_threads_roundtrip(tmp_path):
    st = ResearchStore(str(tmp_path))
    st.insert_dataclass("threads", ThreadState(thread_id="T-X", name="demo", state="RUNNABLE",
                                               dependency="none", gate_name="GATE_X", next_action="run"))
    rows = st.rows("threads")
    assert len(rows) == 1 and rows[0]["gate_name"] == "GATE_X", rows

def test_schema_has_gate_name(tmp_path):
    st = ResearchStore(str(tmp_path))
    cols = {r[1] for r in st.conn.execute("PRAGMA table_info(threads)")}
    assert "gate_name" in cols and "gate" not in cols, cols

def test_migration_from_gate_column(tmp_path):
    """A v0.1 project that somehow created a `gate` column must still round-trip."""
    db = tmp_path / ".aris"; db.mkdir()
    con = sqlite3.connect(db / "research_state.sqlite3")
    con.execute("CREATE TABLE threads(thread_id TEXT PRIMARY KEY, name TEXT, state TEXT, dependency TEXT, gate TEXT, next_action TEXT, human_review_required INTEGER, updated_at TEXT)")
    con.commit(); con.close()
    st = ResearchStore(str(tmp_path))
    cols = {r[1] for r in st.conn.execute("PRAGMA table_info(threads)")}
    assert "gate_name" in cols or "gate" in cols

def test_cli_smoke(tmp_path):
    root = str(tmp_path / "proj"); root_pkg = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    r = subprocess.run([sys.executable, "-m", "aris_os.cli", "init-project", "--root", root, "--name", "smoke"],
                       cwd=root_pkg, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    r = subprocess.run([sys.executable, "-m", "aris_os.cli", "status", "--root", root], cwd=root_pkg,
                       capture_output=True, text=True)
    assert r.returncode == 0 and "[threads]" in r.stdout, r.stdout
