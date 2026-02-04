# define normalisation function
# this function will be called at the start of the graph execution
from src.state.schema import StudentState


def normalise_inputs(state: StudentState) -> dict:
    """validate and normalise input fields"""
    if not state.get("student_name"):
        raise ValueError("Student name is required")
    if not state.get("today"):
        raise ValueError("Today's date is required")
    if not state.get("assignments"):
        state_assignments = []
    else:
        state_assignments = state["assignments"]

    return {
        "assignments": state_assignments, 
        "today_plan": [],
        "pressure_score": 0.0,
        "current_assignment_id": None,
        "rubric": None,
        }