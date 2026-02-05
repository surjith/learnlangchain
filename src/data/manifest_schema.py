from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    doc_type: str           # "rubric" | "assignment_question" | etc.
    path: str               # filesystem path for Lesson 4 (.md/.txt)

@dataclass(frozen=True)
class AssignmentEntry:
    assignment_id: str
    sources: list[Source]

