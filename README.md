# ARIS Research OS v0.1

A local-first research orchestration framework for long-running scientific projects.

## Core idea

Large research projects fail from state loss, stale evidence, version drift, fragmented writing, and unmanaged iteration as often as from analytical limitations.

ARIS Research OS separates:

- **Human PI** — sets scientific direction and approves high-impact decisions.
- **Professor Agent** — orchestrates the project.
- **Executor / ARIS** — runs analyses and experiments.
- **Writer** — maintains the living manuscript from approved evidence only.
- **Reviewer** — challenges claims, consistency, leakage, and overstatement.
- **Literature Curator** — maintains verified external evidence.
- **Figure/Table Curator** — maintains figure/table lineage and manuscript placement.

## Architecture

```text
Human PI
   |
Professor Agent
   |
   +-- Executor
   +-- Writer
   +-- Reviewer
   +-- Literature Curator
   +-- Figure/Table Curator
   |
Research State Store
   +-- decisions
   +-- results
   +-- claims
   +-- gates
   +-- threads
   +-- events
   +-- manuscript state
```

## Why v0.1 is not a full App

The first version is intentionally **repo-first** and **local-first**:

1. Markdown/YAML remain human-readable.
2. SQLite provides machine-queryable state.
3. Skills define agent behavior.
4. CLI provides reproducible orchestration.
5. A web dashboard can be added later without changing the project model.

## Quick start

```bash
python -m aris_os.cli init-project --root D:\MyResearchProject --name "My Project"
python -m aris_os.cli status --root D:\MyResearchProject
python -m aris_os.cli add-event --root D:\MyResearchProject --type result_ready --source executor --summary "E09 completed"
python -m aris_os.cli daily-brief --root D:\MyResearchProject
```

## Canonical lifecycle

```text
EXPLORE
  -> REVIEW
  -> AUTO-CONTINUE or HUMAN REVIEW
  -> DECISION
  -> UPDATE DESIGN
  -> FREEZE
  -> RELEASE GATE
  -> DOWNSTREAM RESUME
```

## Status vocabulary

Threads:

- PLANNED
- RUNNABLE
- RUNNING
- COMPLETE
- PARTIAL
- FAILED_RETAINED
- WAITING_FOR_GATE
- WAITING_FOR_HUMAN_REVIEW
- BLOCKED
- SUPERSEDED

Evidence:

- EXPLORATORY
- CANDIDATE
- APPROVED
- FROZEN
- SUPERSEDED
- REJECTED

## Important rule

The Writer must never treat raw experiment output as manuscript-ready evidence.
Only APPROVED/FROZEN Results and Claims may be promoted to the living manuscript.
