# Execution Preflight Skill v0.2

## Purpose
Verify the execution context before running substantive code.

## Trigger
Immediately before any long-running or authoritative execution.

## Inputs
- `PROJECT_IDENTITY.yaml`
- Task description with read sources, write target, upstream freeze ID, and
  expected output

## Hard constraints
- Return `PREFLIGHT_PASS` before code execution.
- Never proceed on `FAIL`.

## Procedure
1. Verify project ID.
2. Verify root.
3. Verify write target.
4. Verify upstream freeze ID.
5. Verify design fingerprint.
6. Verify destructive operations.
7. Verify input hashes if frozen.
8. Verify no foreign-project path.
9. Verify expected output location.

## Outputs
`PREFLIGHT_PASS` or a list of failed checks.

## Stop conditions
Any failed check.

## Human-review conditions
Destructive operations or ambiguous cross-project inputs.

## Examples
A write target outside the canonical root fails preflight.
