# Release Notes — ARIS Research OS v0.2.0

## Overview

v0.2.0 upgrades ARIS Research OS from an execution-oriented framework into a
convergent, auditable, human-in-the-loop research operating system.

## Major additions

### Project Identity Gate

`PROJECT_IDENTITY.yaml` plus `GATE_PROJECT_IDENTITY` stop execution when a task
targets the wrong project, root, or scientific fingerprint.

### Frozen Executable State

Accepted science is frozen as a complete executable state, including
parameters, fitted objects, runtime-derived objects, code, hashes, and
environment.

### Human-in-the-loop governance

Scientific and irreversible choices are reserved for humans while agents
automate verification, provenance, and audit.

### Research convergence

Research moves `Explore -> Decide -> Audit -> Freeze -> Compress -> Advance`
so accepted state becomes progressively immutable.

### External validation governance

`GATE_EXTERNAL_REPLAY` requires a generic wrapper to replay an accepted
external dataset before a new external database is authorized.

### Incident response

A read-only forensic workflow preserves evidence for cross-project
contamination and provenance failures.

### Reproducibility levels

`R0` through `R5` make reproducibility explicit. Cross-database external
validation requires at least `R5`.

### CLI additions

`bootstrap-project-v02`, `gate-identity`, `preflight`, `freeze-check`,
`external-replay-gate`, `destructive-gate`, `classify-failure`, and
`reproducibility`.

## Migration from v0.1

See [MIGRATION_v0.1_to_v0.2.md](MIGRATION_v0.1_to_v0.2.md).

## Known limitations

See [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md).

## Breaking changes

None for the `aris_os` import namespace or existing v0.1 CLI commands. A
v0.1 example containing project-specific scientific content and the clinical
workflow overlays were removed because they were not appropriate for a public,
general-purpose release.

## Upgrade notes

- The import namespace remains `aris_os`.
- Runtime dependencies remain empty (standard library only).
- `VERSION` and package metadata now read `0.2.0`.
