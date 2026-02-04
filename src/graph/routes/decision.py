from typing import Literal
from src.graph.state.schema import StudentState

def route_by_pressure(state: StudentState) -> Literal["triage_plan", "normal_plan"]:
    """decide which planning strategy to use based on pressure score"""
    return "triage_plan" if state["pressure_score"] >= 1 else "normal_plan"