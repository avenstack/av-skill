"""
Human-in-the-Loop Example

This example demonstrates how to interrupt execution
for human approval before continuing with the workflow.
"""

from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from typing_extensions import TypedDict, Annotated
from typing import List
from operator import add


# Define a potentially sensitive tool
@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to a recipient."""
    return f"Email sent to {to} with subject '{subject}'"


@tool
def execute_command(command: str) -> str:
    """Execute a system command (simulated)."""
    return f"Executed command: {command}"


class State(TypedDict):
    """The state object that flows through the graph."""
    messages: Annotated[List[str], add]


def build_graph() -> StateGraph:
    """Build a graph with human-in-the-loop approval."""
    tools = [send_email, execute_command]
    tool_node = ToolNode(tools)

    def agent(state: State):
        model = ChatAnthropic(model="claude-sonnet-4-5-20250213")
        model_with_tools = model.bind_tools(tools)
        response = model_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    def should_continue(state: State) -> str:
        messages = state["messages"]
        last_message = messages[-1]

        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
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

    # Add memory and interrupt before tools
    memory = MemorySaver()
    return graph.compile(
        checkpointer=memory,
        interrupt_before=["tools"]  # Pause before executing tools
    )


def main():
    """Run the example demonstrating human approval workflow."""
    app = build_graph()
    config = {"configurable": {"thread_id": "approval-thread"}}

    # First interaction
    print("=== Step 1: Initial Request ===")
    result = app.invoke(
        {"messages": [("user", "Send an email to alice@example.com about meeting")]},
        config
    )

    # Check if we're interrupted
    state = app.get_state(config)
    print(f"Next: {state.next}")  # Should show ['tools']
    print(f"Pending tool calls: {len(result['messages'][-1].tool_calls)}")

    # Get human approval
    print("\n=== Step 2: Human Review ===")
    last_message = result["messages"][-1]
    if hasattr(last_message, "tool_calls"):
        for tool_call in last_message.tool_calls:
            print(f"Tool: {tool_call['name']}")
            print(f"Arguments: {tool_call['args']}")

    # Simulate human approval
    print("\nType 'yes' to approve, 'no' to reject:")
    # In real scenario, you would get actual user input here
    # For demo, we'll auto-approve
    approval = "yes"

    if approval.lower() == "yes":
        print("=== Step 3: Resuming with Approval ===")
        # Resume execution (None means continue with current state)
        result = app.invoke(None, config)
        print(f"Final result: {result['messages'][-1].content}")
    else:
        print("=== Request Rejected ===")
        # You could modify state or terminate here
        print("Workflow terminated by user")


if __name__ == "__main__":
    main()
