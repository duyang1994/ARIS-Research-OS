# Result Review Gate Skill v0.2

## Purpose
Enforce audit-before-interpretation ordering for every result review.

## Trigger
Reviewing any agent report or proposed result.

## Inputs
- Agent report or result artifact
- `PROJECT_IDENTITY.yaml`, lineage, freeze provenance, code

## Hard constraints
- Do not begin by interpreting AUROC, p-values, or plots.
- If project identity or lineage fails, stop.

## Procedure
1. PROJECT IDENTITY
2. SCIENTIFIC DESIGN
3. INPUT LINEAGE
4. FREEZE PROVENANCE
5. IMPLEMENTATION
6. RESULT
7. REPRODUCIBILITY
8. INTERPRETATION

## Outputs
A result review header with PASS/FAIL for each gate before narrative.

## Stop conditions
Identity, fingerprint, lineage, or freeze-state failure.

## Human-review conditions
Any result marked for manuscript claim or primary endpoint.

## Examples
A technically successful reproduction of the wrong cohort must fail the
project-identity and lineage checks before its numbers are interpreted.
