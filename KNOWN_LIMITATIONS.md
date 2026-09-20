# Known Limitations

ARIS Research OS is honest about what it cannot guarantee.

- **Governance cannot guarantee scientific correctness.** It can make
  identity, lineage, and freeze state explicit and auditable, but a fully
  passing gate can still describe bad science.
- **Human adjudication remains necessary for scientific redesign.** Cohort,
  endpoint, analysis-unit, and model-strategy changes are human decisions.
- **Adapters to external agent frameworks are still evolving.** ARIS Research
  OS is agent-agnostic, but first-class integrations mature over time.
- **Project identity depends on correctly initialized metadata.** If
  `PROJECT_IDENTITY.yaml` is wrong, the gates can only check against what was
  recorded.
- **Reproducibility depends on the persistence of required artifacts.** A
  missing scaler, checkpoint, or normalization constant cannot be recovered
  from governance rules alone.
- **Bitwise reproducibility is not guaranteed across all hardware and
  software stacks.** The framework records environment and hashes, but does
  not eliminate numerical or platform variation.

## Scope

- This is not a statistical analysis library.
- The dependency-free YAML parser used by the CLI supports a small, controlled
  subset of YAML (flat scalars and indented `- item` lists).
- The framework does not modify user project repositories; it only provides
  templates and a bootstrap command that users run deliberately.

## License

Apache License 2.0. See [LICENSE](LICENSE).
