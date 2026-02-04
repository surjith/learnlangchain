
from src.graph.state.schema import StudentState
from datetime import date, timedelta

'''If there is more than 120 minutes of estimated work due in the next 3 days,
    we consider the student to be under high pressure. Otherwise, the pressure is lower.'''
def calculate_pressure(state: StudentState) -> dict:
    """calculate pressure score based on upcoming assignments"""

    today = date.fromisoformat(state["today"])
    horizon = today + timedelta(days=3)

    total_estimated = sum(
        assignment["est_minutes"] for assignment in state["assignments"]
        if (
            assignment["status"] != "completed"
            and date.fromisoformat(assignment["due_date"]) <= horizon
        )
    )
    pressure_score = min(total_estimated / 120.0, 1.0)  # Normalize to a max of 1.0
    return {"pressure_score": pressure_score}