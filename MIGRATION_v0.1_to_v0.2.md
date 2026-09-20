# Migration from v0.1 to v0.2

Use this workflow when adopting v0.2 for an existing v0.1 project.

1. Identify the canonical project root.
2. Create `PROJECT_IDENTITY.yaml` (human-reviewed, not inferred).
3. Create `design/CURRENT_DESIGN.md` from the accepted v0.1 plan.
4. Create `governance/CONSTRAINTS.yaml`.
5. Reconstruct `governance/DECISION_REGISTER.md` from historical decisions.
6. Identify accepted results and assign stable result IDs.
7. Assign freeze IDs to previously accepted states.
8. Persist parameters and artifacts into the frozen registries.
9. Create `MASTER_INDEX.md`.
10. Create `PROJECT_STATUS.md`.
11. Run a reproducibility audit.
12. Reach the target reproducibility level (`R0` through `R5`).

## Safety rules during migration

- Do not rewrite history. Preserve superseded and failed branches.
- Do not silently "fix" a wrong definition, path, unit, cohort, or model.
  Stop, report, classify, and request or use an authorized decision.
- Do not modify scientific data while scaffolding governance.

## Backward compatibility

- Existing v0.1 Markdown templates and the SQLite state store remain usable.
- The v0.1 CLI commands (`init-project`, `status`, `add-event`,
  `daily-brief`) are preserved.
- v0.2 adds gates and skills rather than removing v0.1 behavior.
