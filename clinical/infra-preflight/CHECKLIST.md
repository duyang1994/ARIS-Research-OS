# P-8 — infrastructure pre-flight (APPROVED WITH TESTING)

Before ANY database-dependent scientific analysis:

1. PostgreSQL reachable (`pg_isready`), expected database and schema present
2. Required tables non-empty with row counts within expected order of magnitude
3. Cohort/cache files present with expected hash and row counts
4. Free disk space above a task-specific floor
5. Any required cached artifact (e.g. `_cache/v2_primary`) readable

If a check fails: status = `BLOCKED_INFRA`, the analysis must not run, and the failure must never be
recorded as a scientific result.

Evidence: CKM2 defect D20 — the manually started PostgreSQL instance had stopped between runs, and
the first M1 attempt silently produced H2/H3 identical to H1 because the survivorship masks could
not be built (kept as `iteration_016_attempt1_PARTIAL_no_db`).
