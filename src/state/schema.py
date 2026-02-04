from typing import Literal, TypedDict, List

Status = Literal["not_started", "in_progress", "completed"]

class Assignement(TypedDict):
    title: str
    subject: str
    due_date: str
    est_minutes: int
    description: str
    status: Status

class StudentState(TypedDict):
    # input fields
    student_name: str
    today: str
    assignments: List[Assignement]

    # output fields
    pressure_score: float
    today_plan: List[str]