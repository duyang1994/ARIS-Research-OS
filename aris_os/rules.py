BLOCKING_EVENT_TYPES = {
    "major_redesign",
    "scientific_definition_change",
    "materially_different_results",
    "primary_endpoint_change",
    "external_validation_change",
}

WRITER_ALLOWED_RESULT_STATUS = {"APPROVED", "FROZEN"}

def requires_human_review(event_type: str) -> bool:
    return event_type in BLOCKING_EVENT_TYPES

def writer_can_use(result_status: str) -> bool:
    return result_status in WRITER_ALLOWED_RESULT_STATUS

def thread_can_run(state: str) -> bool:
    return state in {"RUNNABLE", "RUNNING"}

def downstream_should_pause(gate_status: str) -> bool:
    return gate_status not in {"PASS", "CONDITIONAL_PASS"}
