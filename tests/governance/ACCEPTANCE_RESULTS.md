# Governance Acceptance Test Results

Run with:

```bash
python -m pytest tests/governance -q
```

## Synthetic cases

| Case | Expected | Status |
|---|---|---|
| Execute Project A task using Project B root | `GATE_PROJECT_IDENTITY = FAIL` | `test_cross_project_identity_fails` |
| Matching Project A task | `GATE_PROJECT_IDENTITY = PASS` | `test_matching_identity_passes` |
| Accepted result with unsaved scaler | `GATE_EXECUTABLE_FREEZE = FAIL` | `test_accepted_result_with_unsaved_scaler_fails_freeze` |
| Valid frozen project | `GATE_EXECUTABLE_FREEZE = PASS` | `test_valid_frozen_project_passes` |
| Ephemeral stdin-generated result | `RESULT_STATE = PROVISIONAL` | `test_ephemeral_stdin_result_is_provisional` |
| External validation without replay | `GATE_EXTERNAL_REPLAY = FAIL` | `test_external_validation_without_replay_fails` |
| Destructive operation without approval | `GATE_DESTRUCTIVE_OPERATION = FAIL` | `test_destructive_operation_without_approval_fails` |
| Failure classification | taxonomy mapping | `test_failure_classification` |

The `tests/governance/test_v02_governance.py` module encodes these as
executable assertions so the acceptance criteria are not prose-only.
