# Human / Agent Division of Responsibility

The human decides **what** the science should be. Agents ensure execution
remains consistent with that science.

> The human should not need to inspect hundreds of lines of implementation
> instructions to prevent routine path or configuration errors.

## Human responsibilities

- Choose the scientific question.
- Provide causal and clinical interpretation.
- Authorize cohort and endpoint redesign.
- Set the primary-vs-sensitivity hierarchy.
- Make irreversible choices.
- Approve manuscript claims.
- Decide publication strategy.

## Agent responsibilities

- Implementation.
- Path checking.
- Project identity verification.
- Hash checking.
- Provenance tracing.
- Parameter persistence.
- Reproduction testing.
- Consistency audit.
- Error detection.
- Evidence presentation.

## Shared responsibilities

- Interpretation.
- Sensitivity planning.
- Limitation assessment.
- Claim calibration.

## What the agent verifies before reaching the human

- Project identity and canonical root.
- Write targets and forbidden roots.
- Hash and lineage checks.
- Freeze completeness.
- Reproducibility of a claimed result.

The human then reviews only the compact decision packet, not the full
execution trace, unless the agent explicitly escalates an anomaly.
