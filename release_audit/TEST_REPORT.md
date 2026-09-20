# Test Report

Date: 2026-09-20

## Environment

- Python: 3.10.11
- Test runner: pytest

## Command

```bash
python -m pytest tests/governance -q
```

## Result

```text
8 passed in 0.04s
```

## Counts

| Metric | Count |
|---|---|
| Passed | 8 |
| Failed | 0 |
| Skipped | 0 |

## Coverage

The governance acceptance suite covers:

- cross-project identity (`GATE_PROJECT_IDENTITY` FAIL and PASS),
- accepted result missing a scaler (`GATE_EXECUTABLE_FREEZE` FAIL),
- valid frozen project (`GATE_EXECUTABLE_FREEZE` PASS),
- ephemeral stdin result (`PROVISIONAL`),
- external validation without replay (`GATE_EXTERNAL_REPLAY` FAIL),
- destructive operation without approval (`GATE_DESTRUCTIVE_OPERATION` FAIL),
- failure classification.

## Conclusion

**PASS** — 0 failed tests.
