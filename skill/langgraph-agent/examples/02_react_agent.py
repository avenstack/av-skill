"""
ReAct Agent Example - Tool-Using Agent

This example demonstrates a ReAct (Reason + Act) agent that can use tools
to answer questions and perform actions.
"""

from langgraph.graph import START, StateGraph
from langgraph.prebuilt import ToolNode
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from typing_extensions import TypedDict, Annotated
from typing import List
from operator import add


# Define tools
@tool
def search_engine(query: str) -> str:
    """Search for information about a query."""
    # Simulated search results
    database = {
        "weather": "The weather is sunny with a high of 75°F.",
        "python": "Python is a high-level programming language.",
        "langgraph": "LangGraph is a framework for building stateful agents."
    }
    for key, value in database.items():
        if key in query.lower():
            return value
    return f"No results found for: {query}"


@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        result = eval(expression)
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error evaluating expression: {e}"


class State(TypedDict):
    """The state object that flows through the graph."""
    messages: Annotated[List[str], add]


def build_graph() -> StateGraph:
    """Build and compile a ReAct agent."""
    tools = [search_engine, calculator]
    tool_node = ToolNode(tools)

    # Create agent node
    def agent(state: State):
        model = ChatAnthropic(model="claude-sonnet-4-5-20250213")
        model_with_tools = model.bind_tools(tools)
        response = model_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    # Define routing logic
    def should_continue(state: State) -> str:
        messages = state["messages"]
        last_message = messages[-1]

        # If the last message has tool calls, continue to tools
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        # Otherwise, end
        return END

    # Build graph
    graph = StateGraph(State)
    graph.add_node("agent", agent)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", should_continue, {
        "tools": "tools",
        END: END
    })
    graph.add_edge("tools", "agent")

    return graph.compile()


def main():
    """Run the example."""
    app = build_graph()

    # Example queries
    queries = [
        "What is the weather?",
        "What is 25 * 4 + 10?",
        "Tell me about LangGraph"
    ]

    for query in queries:
        print(f"\n=== Query: {query} ===")
        result = app.invoke({
            "messages": [("user", query)]
        })

        # Print final response
        final_message = result["messages"][-1]
        print(f"Response: {final_message.content}")


if __name__ == "__main__":
    main()
