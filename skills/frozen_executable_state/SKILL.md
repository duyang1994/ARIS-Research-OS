# Frozen Executable State Skill v0.2

## Purpose
Formalize the complete executable state captured at freeze time.

## Trigger
Freeze-on-accept and any reproducibility audit.

## Inputs
- Design state, cohort, contracts, parameters, artifacts, code, environment

## Hard constraints
- All 23 required components must be present before downstream work.
- A missing component means the state is not an executable freeze.

## Procedure
1. Assemble the required components.
2. Hash code and artifacts.
3. Record runtime environment.
4. Include smoke-test input and expected output.
5. Generate an integrity manifest.

## Outputs
A freeze directory containing the complete manifest and artifacts.

## Stop conditions
Missing fitted object, checkpoint, normalization constant, or code.

## Human-review conditions
Any decision about whether an incomplete state may still be used.

## Examples
`GATE_EXECUTABLE_FREEZE` fails when a scaler is missing from the freeze.
