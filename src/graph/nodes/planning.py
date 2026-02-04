# define a funtion to build the plan
from typing import List
from src.graph.state.schema import StudentState

def normal_plan(state: StudentState) -> dict:
    plan = state["today_plan"]
    plan.append("Mode: Normal Planning:\n")
    plan.append("Focus on completing assignments based on due dates and estimated time.\n")
    return {"today_plan": plan}


def triage_plan(state: StudentState) -> dict:
    plan = state["today_plan"]

    plan.append("Mode: ⚠️ Triage")
    plan.append("Too much due soon. Reduce scope.")
    plan.append("Action:")
    plan.append("- Pick ONE task")
    plan.append("- Work 25 minutes")
    plan.append("- Ask teacher if extensions are possible")

    return {"today_plan": plan}