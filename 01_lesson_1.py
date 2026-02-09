from dotenv import load_dotenv
from src.graph.state.schema import StudentState
from src.graph.graph import graph

load_dotenv(override=True)  # Load environment variables from .env file

if __name__ == "__main__":
    # Run the application with an initial state
    app = graph()

    initial = {
    "student_name": "Ananya",
    "today": "2026-02-03",
    "assignments": [
        {
            "id": "eng-001",
            "title": "Persuasive writing draft",
            "subject": "English",
            "due_date": "2026-02-05",
            "est_minutes": 90,
            "status": "not_started",
            "rubric_ref": "src/data/rubrics/english_writing.txt",
        },
        {
            "id": "sci-001",
            "title": "Science glossary",
            "subject": "Science",
            "due_date": "2026-02-05",
            "est_minutes": 95,
            "status": "completed",
            "rubric_ref": None,
        },
        {
            "id": "math-001",
            "title": "Algebra worksheet",
            "subject": "Math",
            "due_date": "2026-02-05",
            "est_minutes": 40,
            "status": "in_progress",
            "rubric_ref": None,
        },
    ],
    }

    final = app.invoke(initial)
    print("\n".join(final["today_plan"]))
