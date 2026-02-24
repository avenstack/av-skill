"""
Basic LangGraph Example - Sequential Chain

This example demonstrates a simple sequential workflow where
each node processes and passes data to the next node.
"""

from langgraph.graph import START, END, StateGraph
from typing_extensions import TypedDict


class State(TypedDict):
    """The state object that flows through the graph."""
    input: str
    processed: str
    output: str


def step1_process_input(state: State) -> dict:
    """First node: Process the input."""
    input_text = state["input"]
    processed = f"Processed: {input_text.upper()}"
    print(f"Step 1: {input_text} -> {processed}")
    return {"processed": processed}


def step2_generate_output(state: State) -> dict:
    """Second node: Generate final output."""
    processed = state["processed"]
    output = f"Final: {processed} + extra transformation"
    print(f"Step 2: {output}")
    return {"output": output}


def build_graph() -> StateGraph:
    """Build and compile the sequential graph."""
    graph = StateGraph(State)

    # Add nodes
    graph.add_node("process", step1_process_input)
    graph.add_node("generate", step2_generate_output)

    # Add edges
    graph.add_edge(START, "process")
    graph.add_edge("process", "generate")
    graph.add_edge("generate", END)

    return graph.compile()


def main():
    """Run the example."""
    app = build_graph()

    # Invoke the graph
    result = app.invoke({
        "input": "Hello LangGraph!",
        "processed": "",
        "output": ""
    })

    print("\n=== Result ===")
    print(result)


if __name__ == "__main__":
    main()
