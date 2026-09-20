# Research Incident Response Skill v0.2

## Purpose
Respond to suspected contamination or provenance failures without destroying
evidence.

## Trigger
Detection of cross-project contamination, wrong root, wrong cohort, or
unexplained provenance mismatch.

## Inputs
- Incident description
- Canonical roots and file inventory

## Hard constraints
- Do not immediately delete suspected contamination.
- Preserve a read-only forensic audit.

## Procedure
DETECT -> STOP -> PRESERVE -> DEFINE BOUNDARY -> READ-ONLY FORENSIC AUDIT ->
CLASSIFY IMPACT -> HUMAN REVIEW -> CONTROLLED RECOVERY -> POST-RECOVERY AUDIT
-> LESSON -> GOVERNANCE UPDATE.

## Outputs
An incident report and a governance update.

## Stop conditions
Any attempt to modify evidence before forensic preservation.

## Human-review conditions
Removal of contamination and any scientific recovery decision.

## Examples
On suspected cross-project contamination: stop writes, identify roots, define
cutoff, inventory files, hash source vs copied artifacts, preserve audit,
remove only human-approved contamination, verify source science unchanged,
restart from canonical state.
