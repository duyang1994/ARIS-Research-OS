# Context Compaction Skill v0.2

## Purpose
Make conversation history secondary to structured state files.

## Trigger
At stage completion or freeze.

## Inputs
- `PROJECT_STATUS.md`
- `MASTER_INDEX.md`
- `CURRENT_DESIGN.md`
- `RESULTS_LEDGER.csv`
- `OPEN_QUESTIONS.md`

## Hard constraints
- Do not depend on chat history.
- The active agent context should be reconstructable primarily from these
  files.

## Procedure
1. Update project status.
2. Update master index.
3. Update current design.
4. Update results ledger.
5. Update open questions.
6. Move historical detail to archive.

## Outputs
Compact, current state files that support context-free resume.

## Stop conditions
Active state files missing required fields.

## Human-review conditions
None by default; this is an agent bookkeeping task.

## Examples
After a freeze, an agent resumes by reading `PROJECT_IDENTITY.yaml`,
`PROJECT_STATUS.md`, `MASTER_INDEX.md`, `CURRENT_DESIGN.md`,
`CONSTRAINTS.yaml`, `DECISION_REGISTER.md`, and the freeze manifest.
