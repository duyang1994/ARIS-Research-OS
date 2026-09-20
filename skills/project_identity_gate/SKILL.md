# Project Identity Gate Skill v0.2

## Purpose
Confirm that a task belongs to the intended project before any substantive
execution. This is the mandatory first gate.

## Trigger
Before any analysis, external validation, freeze, or authoritative write.

## Inputs
- `PROJECT_IDENTITY.yaml`
- Requested project ID and canonical root
- Read sources and write target

## Hard constraints
- If the gate returns `FAIL`, stop immediately. No model execution.
- Do not infer identity from folder names or chat context.

## Procedure
1. Load `PROJECT_IDENTITY.yaml`.
2. Compare project ID and canonical root with the requested task.
3. Check the scientific fingerprint.
4. Verify write target belongs to the current project.
5. Verify inputs belong to the project or are explicitly approved external
   sources.
6. Confirm no forbidden root or foreign signature appears without explanation.

## Outputs
`PASS`, `FAIL`, or `WAITING_FOR_HUMAN_REVIEW` with a check list.

## Stop conditions
Any identity, root, fingerprint, write-target, or input-lineage mismatch.

## Human-review conditions
Missing or ambiguous identity fields that prevent an automated decision.

## Examples
Executing a Project A task with Project B's root must return `FAIL`.
