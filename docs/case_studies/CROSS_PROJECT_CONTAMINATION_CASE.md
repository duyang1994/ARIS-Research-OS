# Case Study: Cross-Project Contamination

This case study is anonymized. It focuses on lessons, not blame.

## Background

Two research projects with similar terminology existed in the same working
environment. Both shared overlapping clinical vocabulary, similar variable
names, and similar analysis stages.

## What happened

An execution task selected the **wrong project root**. Because the pipelines
were structurally similar, the reproduction completed without error and
produced technically correct outputs.

The review process evaluated the outputs against the requested design and
found them plausible. It did not detect that the underlying project was the
wrong one.

## Detection

A human later noticed a discrepancy in a clinical definition that did not
match the intended cohort. This triggered a read-only forensic audit.

## Forensic audit

- Identified the two canonical roots.
- Defined a contamination cutoff.
- Inventoried created and modified files.
- Distinguished newly-created files from pre-existing modified files.
- Compared hashes of source versus copied artifacts.
- Confirmed that the original scientific files were intact.

## Recovery

The derived work was reset to the correct canonical project state. Only
human-approved contamination was removed. Source science was verified
unchanged before restarting.

## Governance upgrade

This incident motivated the v0.2 controls:

- Mandatory `PROJECT_IDENTITY.yaml` with a canonical root lock.
- `GATE_PROJECT_IDENTITY` before substantive execution.
- Forbidden project roots and foreign project signatures.
- Read-only forensic incident workflow.
- Distinction between scientific redesign and provenance failure.

## Key lesson

> Reproducing the wrong pipeline perfectly is still failure.

Project identity precedes reproducibility. A technically successful output is
not automatically scientifically valid.
