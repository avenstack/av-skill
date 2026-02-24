"""
Multi-Agent System Example

This example demonstrates how to coordinate multiple specialized agents
in a single workflow using a router pattern.
"""

from langgraph.graph import START, END, StateGraph
from langchain_anthropic import ChatAnthropic
from typing_extensions import TypedDict
from enum import Enum


class AgentType(Enum):
    """Types of specialized agents."""
    RESEARCHER = "researcher"
    CODER = "coder"
    WRITER = "writer"


class State(TypedDict):
    """The state object that flows through the graph."""
    query: str
    agent_type: str
    result: str


# Define specialized agents
def researcher_agent(state: State) -> dict:
    """Agent specialized in research and information gathering."""
    prompt = f"""You are a research agent. Your task is to:
    1. Gather comprehensive information on the topic
    2. Identify key sources and references
    3. Provide detailed analysis

    Query: {state['query']}

    Provide a thorough research summary:"""

    model = ChatAnthropic(model="claude-sonnet-4-5-20250213")
    response = model.invoke(prompt)
    print(f"[Researcher] Processing: {state['query'][:50]}...")
    return {"result": f"RESEARCH: {response.content}"}


def coder_agent(state: State) -> dict:
    """Agent specialized in coding and technical implementation."""
    prompt = f"""You are a coding agent. Your task is to:
    1. Write clean, efficient code
    2. Follow best practices and patterns
    3. Include comments and documentation

    Query: {state['query']}

    Provide code solution:"""

    model = ChatAnthropic(model="claude-sonnet-4-5-20250213")
    response = model.invoke(prompt)
    print(f"[Coder] Processing: {state['query'][:50]}...")
    return {"result": f"CODE: {response.content}"}


def writer_agent(state: State) -> dict:
    """Agent specialized in writing and content creation."""
    prompt = f"""You are a writing agent. Your task is to:
    1. Create engaging, well-structured content
    2. Use appropriate tone and style
    3. Ensure clarity and coherence

    Query: {state['query']}

    Provide written content:"""

    model = ChatAnthropic(model="claude-sonnet-4-5-20250213")
    response = model.invoke(prompt)
    print(f"[Writer] Processing: {state['query'][:50]}...")
    return {"result": f"CONTENT: {response.content}"}


# Router function
def route_to_agent(state: State) -> str:
    """Route the query to the appropriate specialized agent."""
    query = state["query"].lower()

    # Simple keyword-based routing
    if any(word in query for word in ["code", "function", "api", "implement", "debug"]):
        return AgentType.CODER.value
    elif any(word in query for word in ["write", "article", "blog", "content", "story"]):
        return AgentType.WRITER.value
    else:
        return AgentType.RESEARCHER.value


def build_graph() -> StateGraph:
    """Build and compile the multi-agent system."""
    graph = StateGraph(State)

    # Add all agent nodes
    graph.add_node(AgentType.RESEARCHER.value, researcher_agent)
    graph.add_node(AgentType.CODER.value, coder_agent)
    graph.add_node(AgentType.WRITER.value, writer_agent)

    # Add conditional routing from START
    graph.add_conditional_edges(
        START,
        route_to_agent,
        {
            AgentType.RESEARCHER.value: AgentType.RESEARCHER.value,
            AgentType.CODER.value: AgentType.CODER.value,
            AgentType.WRITER.value: AgentType.WRITER.value
        }
    )

    # All agents lead to END
    graph.add_edge(AgentType.RESEARCHER.value, END)
    graph.add_edge(AgentType.CODER.value, END)
    graph.add_edge(AgentType.WRITER.value, END)

    return graph.compile()


def main():
    """Run the multi-agent example."""
    app = build_graph()

    # Test queries for different agent types
    test_queries = [
        "Implement a binary search algorithm in Python",
        "Write a blog post about the future of AI",
        "Research the latest developments in quantum computing"
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print('='*60)

        result = app.invoke({
            "query": query,
            "agent_type": "",
            "result": ""
        })

        print(f"\nAgent Type: {route_to_agent({'query': query})}")
        print(f"Result Preview: {result['result'][:200]}...")


if __name__ == "__main__":
    main()
