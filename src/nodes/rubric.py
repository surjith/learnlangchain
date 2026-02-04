from src.state.schema import StudentState
from src.tools.documents import load_rubric

def pick_most_urgent_assignmen(state: StudentState) -> dict:
    """Pick the most urgent assignment based on due date"""
    incomplete_assignments = [
        a for a in state["assignments"] if a["status"] != "completed"
    ]
    if not incomplete_assignments:
        return {"current_assignment_id": None}

    most_urgent = min(
        incomplete_assignments,
        key=lambda a: a["due_date"]
    )
    return {"current_assignment_id": most_urgent["id"]}


def load_rubric_for_current_assignment(state: StudentState) -> dict:
    """Load rubric for the current assignment into state"""
    current_id = state["current_assignment_id"]
    if not current_id:
        return {"rubric": None}

    assignment = next(
        (a for a in state["assignments"] if a["id"] == current_id), None
    )
    if not assignment or not assignment.get("rubric_ref"):
        return {"rubric": None}

    rubric_content = load_rubric(assignment["rubric_ref"])
    return {"rubric": rubric_content}

def add_rubric_to_plan(state: StudentState) -> dict:
    plan = state["today_plan"]
    rubric = state["rubric"]

    if not rubric:
        return {"today_plan": plan + ["No rubric available for the current assignment."]}
    
    # keep it short in the plan (avoid dumping whole rubric)
    snippet_lines = [ln.strip() for ln in rubric.splitlines() if ln.strip()][:6]
    snippet = "\n".join(snippet_lines)

    return {"today_plan": plan + [f"Rubric (grading criteria):\n{snippet}"]}
