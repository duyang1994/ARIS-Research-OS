# P-6 — sub-agent write sandbox (APPROVED WITH TESTING)

Default authority for any delegated executor:

* ALLOWED write scope: `experiments/<experiment_id>/<iteration>/` only.
* FORBIDDEN: MASTER_LOG.md, DECISION_REGISTER.md, GATE_REGISTER.md, FORMAL_ANALYSIS_BASELINE.md,
  the main design document, `test/` top level, and Git history (`git add`/`git commit`).
* Delivery gate: the four report files (run_report, results_summary, review_summary, next_actions)
  plus `metrics/provenance.json` must exist before the lead agent reviews and merges.
* Defect ids: lead agent uses `Dxx`; sub-agent uses `S-Dxx` (never mixed).

Evidence: CKM2 defects D15 (sub-agent committed and edited MASTER_LOG), D16 (id collision),
S-D22 (two consecutive zero-artifact deliveries).
