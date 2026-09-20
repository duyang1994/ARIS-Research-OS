# Freeze Parameter Persistence Skill v0.2

## Purpose
Persist every scientifically material parameter at acceptance time.

## Trigger
Whenever a human decision marks a result ACCEPT, PRIMARY, FINAL, or FROZEN.

## Inputs
- Runtime objects produced by the analysis
- `FROZEN_PARAMETER_REGISTRY.csv`
- Producer code and environment

## Hard constraints
- Never assume a material parameter can be recovered later.
- Runtime-derived objects require both a reconstruction procedure and a
  reference snapshot.

## Procedure
1. Enumerate scaler, mean/SD, centroids, thresholds, seeds, model
   parameters/weights, variable order, reference profiles, state-orientation
   rules, process-feature schema, CV configuration, and metric implementation.
2. Record each in the frozen parameter registry with source hash.
3. Persist fitted objects and runtime-derived objects.
4. Freeze reconstruction procedure and reference snapshot.

## Outputs
Completed frozen parameter registry and artifact snapshots.

## Stop conditions
Any required parameter cannot be located.

## Human-review conditions
Missing material parameter requires an explicit decision before acceptance.

## Examples
An accepted result with an unsaved scaler fails `GATE_EXECUTABLE_FREEZE`.
