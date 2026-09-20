# Changelog

All notable changes to ARIS Research OS are recorded here.

## [0.2.0] - 2026-09-20

### Added

- `PROJECT_IDENTITY.yaml` and `GATE_PROJECT_IDENTITY`.
- Canonical project root lock and scientific fingerprinting.
- `FROZEN_EXECUTABLE_STATE` and freeze-on-accept.
- Frozen parameter and artifact registries.
- `GATE_EXECUTABLE_FREEZE`, `GATE_RESULT_REVIEW`,
  `GATE_EXTERNAL_REPLAY`, and `GATE_DESTRUCTIVE_OPERATION`.
- Research convergence and context compaction.
- Results and claim ledgers.
- Human preflight header, human decision packet, and result review header.
- Fourteen governance skills under `skills/`.
- `aris_os/governance.py` and `aris_os/bootstrap.py`.
- CLI commands: `bootstrap-project-v02`, `gate-identity`, `preflight`,
  `freeze-check`, `external-replay-gate`, `destructive-gate`,
  `classify-failure`, and `reproducibility`.
- Governance acceptance tests under `tests/governance/`.
- Public release documentation: `ARCHITECTURE.md`, `QUICKSTART.md`,
  `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `KNOWN_LIMITATIONS.md`,
  `CITATION.cff`, `RELEASE_NOTES_v0.2.0.md`, `PUBLIC_RELEASE_STATUS.md`,
  and `GITHUB_PUBLISH_COMMANDS.md`.

### Changed

- `README.md` rewritten as a public landing page.
- Package metadata upgraded and normalized to version `0.2.0`.
- `KNOWN_LIMITATIONS.md` expanded with honest boundary statements.
- `.gitignore` extended for Python and research-runtime outputs.

### Fixed

- Removed project-specific scientific content (a project-specific example and
  the clinical workflow overlays) that was not appropriate for a public,
  general-purpose release.
- Replaced personal local paths and project-specific dataset names in public
  documentation and examples with synthetic placeholders.

### Security / Governance

- Added Apache License 2.0 (`LICENSE`) and `NOTICE`.
- Resolved the previously open license decision; removed
  `LICENSE_DECISION_REQUIRED.md`.
- Added read-only forensic incident response and destructive-operation
  authorization.
- Implemented lessons from a real cross-project provenance incident: a
  technically successful reproduction of the wrong project is still a
  failure, so project identity now precedes reproducibility.

## [0.1.0]

- Initial local-first research orchestration framework with Markdown/YAML
  templates, a SQLite state store, role skills, and a basic CLI.
