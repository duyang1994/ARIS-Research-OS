# clinical/ — ARIS Clinical Governance Extension (proposal stage, v0.2)

Branch: `clinical-meta-v0.2`（baseline commit `956e770` on `master`）
Status: **PHASE 1 — PROPOSAL ONLY.** No upstream skill file has been modified; no `/meta-apply`
has been executed (the command does not exist in this toolchain, and section 39 of the project
instruction requires explicit human approval before landing).

Source of evidence: the CKM2 project run (`D:\20260916CKM2`), 27 iterations, 13 technical defects,
3 sub-agent governance violations, 5 gates, 17 decisions. See
`D:\20260916CKM2\META_OPTIMIZATION_REPORT.md` and `CLINICAL_WORKFLOW_RETROSPECTIVE.md`.

## Reuse-first rule

Upstream ARIS Research OS already provides: the five-table state store (events/decisions/results/
claims/threads/gates), project templates, and the professor / executor / writer / reviewer /
literature / figure_curator role contracts. This extension **must not duplicate those**.
It adds only the clinical gaps listed below, preferably as *overlays* (checklists, templates,
guards) rather than rewritten skills.

## Proposed overlays (from META_OPTIMIZATION_REPORT.md section 3)

| Directory | Gap | Deliverable type |
|---|---|---|
| `cohort-governance/` | cohort version, cohort hash, inclusion/exclusion freeze, duplicate-patient audit, analysis-unit freeze | checklist + template |
| `definition-freeze/` | guideline source verification, operational definition freeze, chronic vs acute evidence, coding vs laboratory hierarchy | checklist |
| `estimand-audit/` | time zero, landmark, conditioning population, endpoint estimand, censoring, survivorship | checklist |
| `temporal-leakage-audit/` | event-after-outcome, landmark overlap, perimortem trajectory, LOS-derived leakage | checklist (CKM2 T1-T10 as a worked template) |
| `measurement-process-audit/` | informative measurement, missingness as signal, testing intensity, physiology/process decomposition | checklist (CKM2 Model F contract) |
| `clinical-gates/` | definition / cohort / phenotype-validity / temporal-validity / external-transport / manuscript-claim gates | gate templates |
| `decision-register/` | "no silent scientific change without a Decision id" enforcement | adapter proposal |
| `major-redesign/` | automatic detection over 7 design fields | adapter proposal |
| `external-transport/` | non-joint transfer, harmonised schema, direction-level success criteria | checklist |
| `clinical-manuscript-audit/` | claim-result map, forbidden-claim list, pending-result markers | checklist |

## Staged patches

See `PATCHES_PROPOSED.md` in this directory. Suggested landing order (needs human approval):
**P-1 (threads schema bugfix) → P-6 (sub-agent sandbox) → P-7 (step guard) → P-8 (infra probe) →
P-2 (human-review vocabulary) → P-5 (gate templates) → P-3 (cohort/estimand columns) →
P-4 (design-change detector) → P-9 (DAG validator)**.

## Upstream defects found (reproducible)

1. **OS-BUG-1 (blocking)** — `aris_os.models.ThreadState.gate` vs SQLite column `gate_name`:
   `insert_dataclass("threads", …)` raises `sqlite3.OperationalError: table threads has no column named gate`.
2. OS-BUG-2 — no CLI command to insert decisions/results/claims; `status` prints raw rows only.
3. OS-BUG-3 — `init-project` copies templates into the project root without a conflict warning.
4. OS-BUG-4 — `daily-brief` "action required" uses a narrow event-type vocabulary and can silently
   under-report human-review items.

## Review status

`PROVISIONAL REVIEW` — produced by the same model family as the executing agent; not a
cross-model acceptance. Cross-family review is required before landing (instruction section 40).
