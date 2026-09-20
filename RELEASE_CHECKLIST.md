# Release Checklist

Use this checklist before marking ARIS Research OS v0.2 ready for a specific
release target.

## Internal use

- [ ] `VERSION` reads `0.2.0`
- [ ] All v0.2 skills have a `SKILL.md`
- [ ] All v0.2 templates exist and are parseable
- [ ] Governance CLI commands run (`bootstrap-project-v02`, `gate-identity`,
      `preflight`, `freeze-check`, `external-replay-gate`,
      `destructive-gate`)
- [ ] Governance acceptance tests pass under `tests/governance/`
- [ ] Migration guide exists (`MIGRATION_v0.1_to_v0.2.md`)
- [ ] `ARCHITECTURE.md` describes the v0.2 control plane

## Public release

- [ ] `README.md` is complete
- [ ] `QUICKSTART.md` is complete
- [ ] `CHANGELOG.md` includes the v0.2 entry
- [ ] `KNOWN_LIMITATIONS.md` is current
- [ ] `CONTRIBUTING.md` exists
- [ ] Apache-2.0 `LICENSE` present and `NOTICE` current
- [ ] Tests pass in a clean environment
- [ ] No unresolved scientific-data references are bundled in the framework

Do not declare `PUBLIC_RELEASE_READINESS = READY_FOR_PUBLIC_RELEASE` if any of
the above public items are incomplete.
