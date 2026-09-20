# Human in the Loop Skill v0.2

## Purpose
Maximize agent execution and audit while reserving irreversible or scientific
choices for the human.

## Trigger
Any decision that changes science, definitions, or irreversibly mutates state.

## Inputs
- Decision context
- `HUMAN_DECISION_PACKET.md` template

## Hard constraints
- Human intervention required for major redesign, ambiguous clinical
  definition, primary/sensitivity hierarchy, endpoint changes, publication
  claims, and destructive operations.
- Human intervention not required for routine path verification, hash checks,
  reproduction testing, format conversion, non-scientific portability fixes,
  logging, or provenance generation.

## Procedure
1. Determine whether the decision is scientific or irreversible.
2. If human is required, produce a compact decision packet.
3. Present options, consequences, and a recommended default.
4. Wait for an explicit decision before proceeding.

## Outputs
A human decision packet and a recorded decision.

## Stop conditions
Proceeding without required human authorization.

## Human-review conditions
See hard constraints above.

## Examples
Changing the analysis unit from first stay to all stays requires a human
decision and a new freeze ID.
