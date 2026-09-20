# Quickstart

This guide uses a synthetic project only: **Project Alpha**. It contains no
patient data, no real hospital paths, and no real user names.

## 1. Bootstrap governance scaffolding

```bash
python -m aris_os.cli bootstrap-project-v02 --root C:\Research\ProjectAlpha
```

This creates `PROJECT_IDENTITY.yaml`, `PROJECT_STATUS.md`, `MASTER_INDEX.md`,
and the `governance/`, `freezes/`, and `audits/` directories. It does not
modify scientific data and does not infer scientific definitions.

## 2. Complete project identity

Edit `C:\Research\ProjectAlpha\PROJECT_IDENTITY.yaml` and set at minimum:

```yaml
project_id: PROJECT-ALPHA
canonical_root: C:\Research\ProjectAlpha
scientific_question: a fictional question
primary_analysis_unit: a fictional unit
```

## 3. Run the project identity gate

```bash
python -m aris_os.cli gate-identity \
  --root C:\Research\ProjectAlpha \
  --project-id PROJECT-ALPHA \
  --canonical-root C:\Research\ProjectAlpha
```

Expected: `GATE_PROJECT_IDENTITY = PASS`.

A mismatched root must return `FAIL`:

```bash
python -m aris_os.cli gate-identity \
  --root C:\Research\ProjectAlpha \
  --project-id PROJECT-BETA \
  --canonical-root C:\Research\ProjectBeta
```

Expected: `GATE_PROJECT_IDENTITY = FAIL`.

## 4. Run execution preflight

```bash
python -m aris_os.cli preflight \
  --root C:\Research\ProjectAlpha \
  --write-target C:\Research\ProjectAlpha\analysis\stage01 \
  --upstream-freeze-id FREEZE-20260101-0001 \
  --expected-output C:\Research\ProjectAlpha\analysis\stage01\results.json
```

Expected: `EXECUTION_PREFLIGHT = PASS` when the identity and freeze references
are valid.

## 5. Verify a frozen executable state

Create a manifest with every required component, then:

```bash
python -m aris_os.cli freeze-check --manifest freezes\FREEZE-20260101-0001\manifest.yaml
```

A manifest missing a fitted object or runtime-derived object must return
`GATE_EXECUTABLE_FREEZE = FAIL`.

## 6. Check external-validation readiness

```bash
python -m aris_os.cli external-replay-gate \
  --generic-wrapper \
  --reference-replay-pass \
  --prior-freeze-id FREEZE-20260101-0001 \
  --target-database ExternalDatasetC
```

Expected: `GATE_EXTERNAL_REPLAY = PASS` when replay passed. Without replay it
must return `FAIL`.

## 7. Check a destructive operation

```bash
python -m aris_os.cli destructive-gate \
  --operation delete \
  --target C:\Research\ProjectAlpha\analysis\stage01 \
  --authorized \
  --decision-id D-0001
```

Without `--authorized` and a decision ID, the gate must return
`GATE_DESTRUCTIVE_OPERATION = FAIL`.

## 8. Resolve reproducibility levels

```bash
python -m aris_os.cli reproducibility --level R5
```

Expected: `EXTERNALIZATION_VERIFIED`.
