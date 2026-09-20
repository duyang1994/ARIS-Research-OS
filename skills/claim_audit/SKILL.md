# Claim Audit Skill v0.2

## Purpose
Connect manuscript claims to accepted evidence and prevent overstatement.

## Trigger
Before promoting or revising a manuscript claim.

## Inputs
- `CLAIM_LEDGER.csv`
- `RESULTS_LEDGER.csv`
- Approved results and freezes

## Hard constraints
- A claim may cite only ACCEPTED or FROZEN results.
- Every claim must record allowed and forbidden wording.

## Procedure
1. Locate the claim in the claim ledger.
2. Verify each evidence result ID is authoritative.
3. Check evidence strength against wording.
4. Flag overstatement and forbidden wording.
5. Record the review.

## Outputs
Updated claim ledger and a claim review result.

## Stop conditions
Claim backed by SUPERSEDED, REJECTED, or PROVISIONAL evidence.

## Human-review conditions
Publication claims and primary claims always require human approval.

## Examples
A claim citing a provisional stdin-generated result is blocked until the
result becomes versioned and accepted.
