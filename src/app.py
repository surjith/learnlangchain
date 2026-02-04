from langgraph.graph import StateGraph, START, END
from src.nodes.normalise import normalise_inputs
from src.nodes.planning import build_plan
from src.state.schema import StudentState

def app() -> StateGraph:
    # build the state graph
    graph = StateGraph(StudentState)

    # add nodes to the graph
    graph.add_node("normalise_inputs", normalise_inputs)
    graph.add_node("build_plan", build_plan)

    # add edges to the graph
    graph.add_edge(START, "normalise_inputs")
    graph.add_edge("normalise_inputs", "build_plan")
    graph.add_edge("build_plan", END)

    return graph.compile()