# Release Cleanup Log

Date: 2026-09-20

## Removed (release-inappropriate or generated)

- A project-specific example directory — project-specific scientific example.
- `clinical/README.md`, `clinical/infra-preflight/CHECKLIST.md`,
  `clinical/step-contract/TEMPLATE.md`, `clinical/subagent-sandbox/CONTRACT.md`,
  `clinical/tests/test_state_store.py` — clinical overlays referencing private
  scientific content.
- `config/project.example.yaml` and `schemas/research_event.schema.json` —
  dormant v0.1 examples not part of the v0.2 public surface.
- `governance/` reference directory — duplicated templates and included a
  local machine path; per-project governance is generated from `templates/`.
- `LICENSE_DECISION_REQUIRED.md` — license decision resolved to Apache-2.0.
- `ARIS_RESEARCH_OS_V0_2_UPGRADE_REPORT.md` — superseded by the public
  release audit.
- `docs/ARCHITECTURE.md` — replaced by root `ARCHITECTURE.md`.

## Generated cache files

`__pycache__/`, `*.pyc`, and `.pytest_cache/` are excluded from version
control by `.gitignore`. No tracked generated files remain.

## Empty directories

Physical empty directories left behind after file removal (`clinical/`,
`config/`, `governance/`, `schemas/`) are not tracked by Git and do not appear
in the release tree.

## Conclusion

No authoritative files were removed.
