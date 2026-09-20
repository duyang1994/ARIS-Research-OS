# File Tree Governance Skill v0.2

## Purpose
Prevent incorrect cross-project path usage.

## Trigger
Before any write or delete.

## Inputs
- Canonical root
- Raw data roots, derived-data roots, write-allowed roots, write-forbidden
  roots, external source roots

## Hard constraints
- Verify paths before writing.
- Cross-project writes require explicit human authorization.

## Procedure
1. Resolve the canonical root.
2. Classify the target as allowed or forbidden.
3. Verify the resolved absolute target stays within scope.
4. Stop if the target is foreign or forbidden.

## Outputs
An explicit allowed/forbidden path decision.

## Stop conditions
Any foreign root, forbidden root, or cross-project write without
authorization.

## Human-review conditions
Cross-project reads/writes and destructive operations.

## Examples
Writing derived artifacts into another project's root is a provenance failure.
