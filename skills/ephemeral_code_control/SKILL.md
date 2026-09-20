# Ephemeral Code Control Skill v0.2

## Purpose
Prevent ephemeral helper code from silently becoming authoritative science.

## Trigger
Whenever stdin helpers, temporary notebooks, or unsaved interactive commands
produce results.

## Inputs
- The ephemeral code and its outputs

## Hard constraints
- Stdin helper outputs are PROVISIONAL.
- Temporary notebooks are PROVISIONAL.
- Unsaved interactive commands are PROVISIONAL.
- These may be used for exploration but may not support manuscript claims,
  external validation, freeze, or final decisions until converted to
  versioned code.

## Procedure
1. Mark the result PROVISIONAL.
2. Save the code to a versioned file.
3. Hash the code.
4. Replay the code to confirm the result.
5. Promote only after replay succeeds.

## Outputs
Versioned, hashed, replayed code and an updated status.

## Stop conditions
Promoting provisional output to authoritative use.

## Human-review conditions
No human review is required to classify code as provisional; promotion to
accepted state follows the normal result-review gate.

## Examples
A result generated from an unsaved shell `python -c` one-liner is PROVISIONAL
until saved, versioned, hashed, and replayed.
