from langgraph.graph import StateGraph, START, END
from src.graph.routes.decision import route_by_pressure
from src.graph.nodes.rubric import pick_most_urgent_assignmen, load_rubric_for_current_assignment, add_rubric_to_plan
from src.graph.nodes.calculate_pressure import calculate_pressure
from src.graph.nodes.normalise import normalise_inputs
from src.graph.nodes.planning import normal_plan, triage_plan
from src.graph.state.schema import StudentState

def graph() -> StateGraph:
    # build the state graph
    graph = StateGraph(StudentState)

    # add nodes to the graph
    graph.add_node("normalise_inputs", normalise_inputs)
    graph.add_node("pressure", calculate_pressure)
    graph.add_node("pick_most_urgent_assignment", pick_most_urgent_assignmen)
    graph.add_node("load_rubric_for_current_assignment", load_rubric_for_current_assignment)
    graph.add_node("add_rubric_to_plan", add_rubric_to_plan)
    graph.add_node("normal_plan", normal_plan)
    graph.add_node("triage_plan", triage_plan)

    # add edges to the graph
    graph.add_edge(START, "normalise_inputs")
    graph.add_edge("normalise_inputs", "pressure")    

    graph.add_conditional_edges(
        "pressure",
        route_by_pressure,
        {
            "triage_plan": "triage_plan",
            "normal_plan": "normal_plan",
        }
    )

    graph.add_edge("normal_plan", END)

    graph.add_edge("triage_plan", "pick_most_urgent_assignment")
    graph.add_edge("pick_most_urgent_assignment", "load_rubric_for_current_assignment")
    graph.add_edge("load_rubric_for_current_assignment", "add_rubric_to_plan")
    graph.add_edge("add_rubric_to_plan", END)

    return graph.compile()