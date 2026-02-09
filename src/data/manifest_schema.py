from dataclasses import dataclass
from typing import Literal

@dataclass(frozen=True)
class Source:
    doc_type: str           # "rubric" | "assignment_question" | etc.
    path: str               # filesystem path for Lesson 4 (.md/.txt)

@dataclass(frozen=True)
class AssignmentEntry:
    assignment_id: str
    sources: list[Source]

@dataclass
class RetrievalResult:
    text: str | None
    num_chunks: int
    avg_distance: float | None
    source: Literal["rubric", "assignment_question", "none"]
