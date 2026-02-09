from __future__ import annotations
from typing import Any, Dict, Literal

RetrievalQuality = Literal["strong", "weak", "none"]

def evaluate_retrieval_quality(state: Dict[str, Any]) -> Dict[str, Any]:
    rr = state.get("retrieval_result")
    if rr is None or rr.text is None or rr.num_chunks == 0:
        return {
            "retrieval_quality": "none",
            "retrieval_debug": {"reason": "no_chunks_or_no_text"},
        }

    avg = rr.avg_distance
    if avg is None:
        return {
            "retrieval_quality": "weak",
            "retrieval_debug": {"reason": "no_distance"},
        }

    # Heuristics (tune later)
    if rr.num_chunks >= 2 and rr.source == "rubric":
        return {
            "retrieval_quality": "strong",
            "retrieval_debug": {"avg_distance": avg, "num_chunks": rr.num_chunks, "source": rr.source},
        }

    # If we only found assignment_question fallback, treat as weak by default
    return {
        "retrieval_quality": "weak",
        "retrieval_debug": {"avg_distance": avg, "num_chunks": rr.num_chunks, "source": rr.source},
    }

def add_generic_guidance_to_plan(state: Dict[str, Any]) -> Dict[str, Any]:
    plan = state.get("today_plan") or []
    addition = (
        "Rubric note: I couldn't find a clear rubric. "
        "I'll use standard expectations: clear structure, evidence, clarity, and checking for errors. "
        "If you have a rubric, upload it for more precise guidance."
    )
    return {"today_plan": plan + [addition]}

def add_missing_rubric_warning(state: Dict[str, Any]) -> Dict[str, Any]:
    plan = state.get("today_plan") or []
    addition = (
        "Rubric note: No rubric or marking criteria was retrieved for this assignment. "
        "Plan will be generic. If this is wrong, add a rubric file or paste criteria into the assignment."
    )
    return {"today_plan": plan + [addition]}

def route_by_retrieval_quality(state: Dict[str, Any]) -> str:
    q = state.get("retrieval_quality", "none")
    if q == "strong":
        return "strong"
    if q == "weak":
        return "weak"
    return "none"
