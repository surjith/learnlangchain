# define a funtion to build the plan
from typing import List
from src.state.schema import StudentState


def build_plan(state: StudentState) -> dict:
    """build a study plan for the day based on assignments"""
    plan: List[str] = []
    name = state["student_name"]
    today = state["today"]
    assignments = state["assignments"]

    plan.append(f"Study plan for {name} on {today}:\n")

    if not assignments:
        plan.append("No assignments for today! Enjoy your day off!")
        plan.append("Remember to review your notes and prepare for upcoming lessons.")
        plan.append("\n")

        plan.append("Action: Add upcoming assignments to get reminders and plans!")
        return {"today_plan": plan}
    
    sorted_assignments = sorted(assignments, key=lambda x: x["due_date"])

    plan.append("Prioritised Assignments by Due Date:\n")
    for assignment in sorted_assignments:
        status = assignment["status"]
        plan.append(
            f"- {assignment['title']} ({assignment['subject']}) - Due: {assignment['due_date']} - Estimated Time: {assignment['est_minutes']} mins - Status: {status}"
        )
    plan.append("\n")
    next_assignment = next((a for a in sorted_assignments if a["status"] != "completed"), None)

    if next_assignment:
        plan.append(
            f"Next Assignment to focus on: {next_assignment['title']} ({next_assignment['subject']}) due on {next_assignment['due_date']} for 20 minutes to get going."
        )
    else:
        plan.append("All assignments are completed! Great job!")
        plan.append("Take a 10 mins break and consider reviewing your notes or preparing for upcoming lessons.")
    
    return {"today_plan": plan}