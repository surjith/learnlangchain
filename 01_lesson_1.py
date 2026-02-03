from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv(override=True)  # Load environment variables from .env file

class State(TypedDict):
    message: str

def hello_node(state: State) -> dict:
    incoming_message = state['message']
    # what happens to the message is not determined in the node itself
    return {"message": incoming_message + f"Hello from the hello_node!"}

# Define the state graph
graph = StateGraph(State)
graph.add_node("hello_node", hello_node)
# graph.add_edge(START, "hello_node")
# graph.add_edge("hello_node", END)
graph.set_entry_point("hello_node")
graph.set_finish_point("hello_node")

app = graph.compile()  # Create the application from the graph

if __name__ == "__main__":
    # Run the application with an initial state
    initial_state: State = {"message": "Hello world! "}
    final_state = app.invoke(initial_state)
    print(final_state)  # Output the final state after processing through the graph
