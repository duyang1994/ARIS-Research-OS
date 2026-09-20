# Canonical Project Tree

Recommended structure for a single ARIS research project. The root contains a
small number of authoritative navigational files; detail is pushed into
subdirectories.

```text
project/
|
├── PROJECT_IDENTITY.yaml
├── PROJECT_STATUS.md
├── MASTER_INDEX.md
|
├── governance/
│   ├── DECISION_REGISTER.md
│   ├── GATE_REGISTER.md
│   ├── DESIGN_CHANGELOG.md
│   ├── MASTER_LOG.md
│   ├── CONSTRAINTS.yaml
│   └── INCIDENT_REGISTER.md
|
├── design/
│   ├── CURRENT_DESIGN.md
│   ├── POPULATION_DEFINITION.md
│   ├── OUTCOME_DEFINITION.md
│   └── ANALYSIS_PLAN.md
|
├── data_contract/
│   ├── INPUT_CONTRACT.md
│   ├── VARIABLE_DICTIONARY.csv
│   └── UNIT_CONTRACT.csv
|
├── analysis/
│   ├── stage01_...
│   ├── stage02_...
│   └── ...
|
├── freezes/
│   └── FREEZE-YYYYMMDD-ID/
|
├── manuscript/
|
├── audits/
|
├── incidents/
|
└── archive/
```

## Rules

- `PROJECT_IDENTITY.yaml`, `PROJECT_STATUS.md`, and `MASTER_INDEX.md` are the
  authoritative active-state entry points.
- `governance/` holds the decision and gate trail.
- `freezes/` holds immutable, complete executable states.
- `audits/` and `incidents/` hold forensic evidence; do not delete them.
- `archive/` holds superseded or historical detail that is no longer active.
