# Contributing

Thanks for helping ARIS Research OS converge. Contributions should strengthen
governance, auditability, and safe human-in-the-loop behavior.

## Bug reports

Report a bug with:

- observed behavior,
- expected behavior,
- minimal reproduction,
- the relevant gate, skill, or template,
- Python version and platform.

If the bug is a provenance or scientific-identity issue, do not silently fix
it in the report; classify it using the failure taxonomy.

## Governance-rule proposals

New governance rules are welcome, but they are high-impact. Every proposal
must include:

1. **Problem** — the concrete failure being addressed.
2. **Failure mode** — how the problem currently manifests.
3. **Proposed constraint** — the exact rule or gate.
4. **Human impact** — what new human decisions or reviews are introduced.
5. **Compatibility** — backward-compatibility and migration notes.
6. **Tests** — how the rule will be verified.

## New skills

Each skill lives in `skills/<name>/SKILL.md` and must contain:

- purpose
- trigger
- inputs
- hard constraints
- procedure
- outputs
- stop conditions
- human-review conditions
- examples

Add the skill to [skills/README.md](skills/README.md).

## Tests

- Governance behavior is tested under `tests/governance/`.
- Run `python -m pytest tests/governance -q` before submitting.
- A public release requires zero failing tests.

## Documentation

Keep the active state compact and link to authoritative detail. Do not add
real patient data, real local paths, or private project names to examples.

## Code of conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
