# Architecture Notes

## v0.1: local-first control plane

**Recommended now**
- Markdown/YAML for human-readable project truth.
- SQLite for machine-readable state.
- Git for version history.
- Skills for role behavior.
- CLI for state transitions and briefs.

**Do not build first**
- complex multi-user SaaS
- custom vector database
- autonomous cloud scheduler
- elaborate web dashboard

These should wait until the workflow survives multiple real projects.

## v0.2 candidate
- event watcher
- dependency graph engine
- stale dependency scanner
- automatic manuscript task creation
- structured JSON event protocol between agents

## v0.3 candidate
- local web dashboard (FastAPI + lightweight frontend)
- project portfolio view
- daily/weekly PI brief
- cross-project workflow lesson promotion

## v1.0 candidate
- reusable Skill package
- pluggable executor/writer/reviewer agents
- role-based permissions
- project templates
- automated project bootstrap
