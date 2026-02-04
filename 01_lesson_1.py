from dotenv import load_dotenv
from src.state.schema import StudentState
from src.app import app

load_dotenv(override=True)  # Load environment variables from .env file

if __name__ == "__main__":
    # Run the application with an initial state
    app = app()

    initial: StudentState = {
        "student_name": "Ananya",
        "today": "2026-02-03",
        "assignments": [
            {"title": "Algebra worksheet", "subject": "Math", "due_date": "2026-02-05", "est_minutes": 45, "status": "in_progress"},
            {"title": "Persuasive writing draft", "subject": "English", "due_date": "2026-02-06", "est_minutes": 90, "status": "not_started"},
            {"title": "Science glossary", "subject": "Science", "due_date": "2026-02-10", "est_minutes": 30, "status": "not_started"},
        ],
        "today_plan": [],
    }

    final = app.invoke(initial)
    print("\n".join(final["today_plan"]))
