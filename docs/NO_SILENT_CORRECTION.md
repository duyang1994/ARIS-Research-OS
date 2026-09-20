# No Silent Correction

If an agent finds a wrong definition, path, unit, cohort, model, or
reference, it must not silently "fix" it.

The agent must:

1. STOP.
2. REPORT the discrepancy.
3. CLASSIFY it using the v0.2 failure/change taxonomy:
   `SCIENTIFIC_REDESIGN`, `REPRODUCIBILITY_GAP`,
   `INFRASTRUCTURE_FAILURE`, `DATA_AVAILABILITY_LIMITATION`,
   `IMPLEMENTATION_BUG`, or `PROVENANCE_FAILURE`.
4. REQUEST or USE an authorized decision.

The only exception is a purely mechanical correction that is explicitly
pre-authorized. Even then, the correction must be logged, not hidden.

Reason: silently changing a definition, path, unit, cohort, model, or
reference destroys the audit trail and can make the project look correct
while being wrong in a way that is no longer detectable.
