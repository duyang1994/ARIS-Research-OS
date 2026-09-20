# Provenance Audit Skill v0.2

## Purpose
Trace every authoritative artifact to its inputs, code, parameters, and freeze.

## Trigger
Before acceptance, freeze, external validation, or forensic recovery.

## Inputs
- `FROZEN_ARTIFACT_REGISTRY.csv`
- `FROZEN_PARAMETER_REGISTRY.csv`
- Producer scripts and hashes

## Hard constraints
- No authoritative object may exist only in RAM, a notebook kernel, a
  workspace, a temporary dataframe, a shell session, a stdin helper, a
  temporary script, or an interactive console.

## Procedure
1. Identify the artifact.
2. Trace producer script and version.
3. Trace input artifacts and parameter registry IDs.
4. Verify hashes.
5. Confirm the artifact is saved, versioned, hashed, and replayed.

## Outputs
A provenance report with hash and lineage evidence.

## Stop conditions
Any missing or unexplained hash or lineage link.

## Human-review conditions
Ambiguous provenance that could affect a scientific claim.

## Examples
An artifact with no saved producer script is PROVISIONAL and cannot support a
manuscript claim.
