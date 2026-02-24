"""
Memory and Persistence Example

This example demonstrates how to add conversation memory
and state persistence to a LangGraph agent.
"""

from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_anthropic import ChatAnthropic
from typing_extensions import TypedDict, Annotated
from typing import List
from operator import add


class State(TypedDict):
    """The state object that flows through the graph."""
    messages: Annotated[List[str], add]


def chatbot_node(state: State):
    """Simple chatbot node that responds to messages."""
    model = ChatAnthropic(model="claude-sonnet-4-5-20250213")
    response = model.invoke(state["messages"])
    return {"messages": [response]}


def build_graph() -> StateGraph:
    """Build and compile a graph with memory."""
    graph = StateGraph(State)
    graph.add_node("chatbot", chatbot_node)
    graph.add_edge(START, "chatbot")
    graph.add_edge("chatbot", START)

    # Add memory
    memory = MemorySaver()
    return graph.compile(checkpointer=memory)


def main():
    """Run the example demonstrating conversation memory."""
    app = build_graph()

    # Create a conversation thread
    config = {"configurable": {"thread_id": "conversation-1"}}

    # Multi-turn conversation
    conversations = [
        "Hi, my name is Alice!",
        "What's my name?",
        "I'm learning about LangGraph.",
        "What did I say I'm learning?"
    ]

    for user_message in conversations:
        print(f"\n=== User: {user_message} ===")

        # Invoke with config for conversation continuity
        result = app.invoke(
            {"messages": [("user", user_message)]},
            config
        )

        # Get and display response
        assistant_message = result["messages"][-1]
        print(f"Assistant: {assistant_message.content}")

    # Show conversation history
    print("\n=== Conversation History ===")
    state = app.get_state(config)
    for i, message in enumerate(state.values["messages"]):
        role = getattr(message, "role", "unknown")
        content = message.content if hasattr(message, "content") else str(message)
        print(f"{i+1}. [{role}] {content}")


if __name__ == "__main__":
    main()
