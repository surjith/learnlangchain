import json
from pathlib import Path
from src.data.manifest_schema import AssignmentEntry, Source

def load_rubric(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def load_text_file(path: Path) -> str:
    """Load .txt or .md as raw text."""
    return path.read_text(encoding="utf-8", errors="replace")

def load_manifest(manifest_path: str) -> list[AssignmentEntry]:
    data = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    entries: list[AssignmentEntry] = []

    for item in data:
        assignment_id = item["assignment_id"]
        sources = [Source(**s) for s in item.get("sources", [])]
        entries.append(AssignmentEntry(assignment_id=assignment_id, sources=sources))

    return entries