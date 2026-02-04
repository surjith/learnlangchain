from typing import Literal, Optional, TypedDict, List

Status = Literal["not_started", "in_progress", "completed"]

class Assignement(TypedDict):
   id: str
   title: str
   subject: str
   due_date: str
   est_minutes: int
   status: Literal["not_started", "in_progress", "completed"]
   rubric_ref: str | None

class StudentState(TypedDict):
    # input fields
    student_name: str
    today: str
    assignments: List[Assignement]

    # Working selections (derived)
    current_assignment_id: Optional[str]
   
    # Derived
    pressure_score: float
    today_plan: List[str]

    # Rubric working context (loaded only when needed)
    rubric: Optional[str]