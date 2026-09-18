from .rules import requires_human_review

class ProfessorOrchestrator:
    """
    v0.1: deterministic control-plane logic.
    This class does not call an LLM. It decides routing/state transitions.
    """

    def route_event(self, event_type: str):
        if requires_human_review(event_type):
            return {
                "action": "HUMAN_REVIEW",
                "pause_scope": "AFFECTED_THREAD_ONLY",
                "parallel_threads": "CONTINUE_IF_INDEPENDENT"
            }
        if event_type in {"result_ready", "figure_ready", "writer_update", "review_issue"}:
            return {"action": "PROFESSOR_REVIEW"}
        return {"action": "AUTO_CONTINUE"}

    def on_decision_approved(self):
        return [
            "UPDATE_DECISION_REGISTER",
            "UPDATE_DESIGN_DOCUMENT",
            "UPDATE_RESULT_OR_CLAIM_STATUS",
            "RECHECK_GATES",
            "RELEASE_ELIGIBLE_THREADS",
            "CREATE_WRITING_TASK_IF_NEEDED",
            "RUN_STALE_DEPENDENCY_CHECK",
        ]
