# P-7 — delegated task step contract (APPROVED WITH TESTING)

Every delegated or scripted step must declare:

| Field | Meaning |
|---|---|
| allowed read scope | exact tables/paths/columns |
| allowed write scope | exact directory (default `experiments/<id>/<iteration>/`) |
| expected outputs | file names + row/column expectations |
| completion criteria | assertions that must hold (row counts, uniqueness, hash equality) |
| failure state | `FAILED_RETAINED` with the failing step recorded; never silently continue |

Runtime guards: `step_guard(expected_rows, expected_cols, max_seconds)`; a shape smoke test before
any model training; row/column assertions in every extraction step.

Evidence: CKM2 defects D1 (missing final SELECT), D2 (4x full-table scans), D4 (cartesian join),
D12/D13/D17/D18 (length/shape), D14 (subset rows in a full-cohort matrix).
