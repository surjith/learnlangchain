from src.graph.state.schema import StudentState
from src.tools.rubric_retriever import RubricRetriever


retriever = RubricRetriever(host="localhost", port=8000, collection_name="rubrics")

def pick_most_urgent_assignmen(state: StudentState) -> dict:
    """Pick the most urgent assignment based on due date"""
    incomplete_assignments = [
        a for a in state["assignments"] if a["status"] != "completed"
    ]
    if not incomplete_assignments:
        return {"current_assignment_id": None}

    most_urgent = min(
        incomplete_assignments,
        key=lambda a: (a["due_date"], -a["est_minutes"])
    )
    return {"current_assignment_id": most_urgent["id"]}


def load_rubric_for_current_assignment(state: StudentState) -> dict:
    """Load rubric for the current assignment into state"""
    assignment_id  = state["current_assignment_id"]
    if not assignment_id :
        return {
            "rubric": None,
            "retrieval_result": None,
        }

    snippet = retriever.retrieve_rubric_snippet(
        assignment_id=assignment_id,
        query="assessment rubric marking criteria success criteria "
        "what teachers look for how marks are awarded",
        k=5,
    )

     # rubric_text stays temporary working data
    return {
        "rubric": snippet.text,          # still temporary
        "retrieval_result": snippet,          # evidence for next node
    }

def add_rubric_to_plan(state: StudentState) -> dict:
    plan = state["today_plan"]
    rubric = state.get("rubric")

    if not rubric:
        return {"today_plan": plan + ["No rubric available for the current assignment."]}
    
    # keep it short in the plan (avoid dumping whole rubric)
    snippet_lines = [ln.strip() for ln in rubric.splitlines() if ln.strip()][:10]
    snippet = "\n".join(snippet_lines)

    return {"today_plan": plan + [f"Rubric (grading criteria):\n{snippet}"]}
