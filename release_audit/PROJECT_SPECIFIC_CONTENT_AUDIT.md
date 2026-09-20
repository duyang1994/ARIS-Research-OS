# Project-Specific Content Audit

Date: 2026-09-20

## Searched terms

Searched terms were project identifiers, cohort descriptors, window terms,
and external dataset names associated with prior private work. For this
public report they are not reproduced verbatim.

## Findings

- A project-specific example and the clinical workflow overlays contained
  private scientific defaults and local paths. They were **removed** as
  release-inappropriate.
- The generic config and schema examples were removed to keep the public root
  clean.
- No remaining hard-coded global governance default encodes a specific
  research project's scientific design.
- Release notes and changelog describe the removals without naming private
  project identifiers.

## Remaining classified occurrences

- `ExternalDatasetC` in a test and `External Dataset A/B` in a skill example
  are explicitly labeled synthetic external-dataset names.
- `examples/project_alpha` uses fictional values only.

## Conclusion

**PASS** — no private scientific data or project-specific defaults remain in
public release content.
