# External Validation Governance Skill v0.2

## Purpose
Ensure external validation begins only from a complete, accepted freeze.

## Trigger
Before applying a model or analysis to an external database.

## Inputs
- `PROJECT_IDENTITY.yaml`
- Current freeze ID and frozen executable state
- Generic externalization wrapper
- Replay result for an already accepted external dataset

## Hard constraints
- External validation may begin only if identity, freeze, externalization,
  replay, and input contract all pass.
- No external database may redefine model, scaler, centroid, threshold, or
  state orientation unless refitting is explicitly part of the design.

## Procedure
1. Confirm project identity.
2. Confirm current freeze ID and executable state.
3. Confirm generic wrapper.
4. Replay an already accepted external dataset.
5. Authorize the new database only after replay passes.

## Outputs
`GATE_EXTERNAL_REPLAY` result and an external-validation readiness record.

## Stop conditions
Replay failure or missing freeze.

## Human-review conditions
Any request to refit on external data.

## Examples
Discovery Dataset -> accepted External Dataset A -> generic wrapper replays
External Dataset A (PASS) -> new External Dataset B authorized.
