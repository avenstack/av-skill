# LangGraph Agent Developer Skill

A comprehensive skill for building stateful, multi-step AI agents using LangGraph - the low-level orchestration framework for building resilient language agents as graphs.

## What is LangGraph?

LangGraph is a framework for building stateful, multi-actor applications with LLMs, built on top of LangChain. It provides:

- **Durable Execution**: Build agents that persist through failures and can run for extended periods
- **Human-in-the-Loop**: Seamlessly incorporate human oversight at any point
- **Comprehensive Memory**: Create truly stateful agents with working and long-term memory
- **Streaming**: Real-time token streaming and step-by-step execution updates
- **Multi-Agent Systems**: Coordinate multiple specialized agents in single workflows

## Quick Start

### Installation

```bash
pip install langgraph langchain-anthropic langchain-core
```

### Basic Example

```python
from langgraph.graph import START, StateGraph
from langchain_anthropic import ChatAnthropic
from typing_extensions import TypedDict

class State(TypedDict):
    messages: list

def agent(state: State):
    model = ChatAnthropic(model="claude-sonnet-4-5-20250213")
    response = model.invoke(state["messages"])
    return {"messages": [response]}

graph = StateGraph(State)
graph.add_node("agent", agent)
graph.add_edge(START, "agent")
app = graph.compile()

result = app.invoke({"messages": [("user", "Hello!")]})
```

## Directory Structure

```
langgraph-agent/
├── SKILL.md                      # Main skill documentation
├── agents/
│   └── openai.yaml              # Agent interface configuration
├── references/
│   └── official-docs-index.md   # Indexed links to official docs
├── examples/
│   ├── README.md                # Example descriptions
│   ├── 01_sequential_chain.py   # Basic sequential workflow
│   ├── 02_react_agent.py        # Tool-using ReAct agent
│   ├── 03_memory_persistence.py # Conversation memory example
│   ├── 04_human_in_the_loop.py  # Human approval workflow
│   └── 05_multi_agent.py        # Multi-agent coordination
└── requirements.txt              # Python dependencies
```

## Core Concepts

### State

The central object that flows between nodes:

```python
class State(TypedDict):
    query: str                    # Single value
    messages: Annotated[list, add]  # Accumulates across nodes
    context: str | None           # Optional
```

### Graph

Define workflows with StateGraph:

```python
graph = StateGraph(State)
graph.add_node("node_name", node_function)
graph.add_edge(START, "node_name")
graph.add_conditional_edges("node", routing_function)
app = graph.compile()
```

### Nodes

Functions that process and update state:

```python
def my_node(state: State) -> dict:
    # Process state
    # Return updated fields
    return {"field": new_value}
```

## Common Patterns

### ReAct Agent

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model="claude-sonnet-4-5-20250213",
    tools=[tool1, tool2],
    checkpointer=MemorySaver()
)
```

### Multi-Agent System

Coordinate specialized agents with conditional routing:

```python
def route_to_agent(state: State) -> str:
    if "code" in state["query"]:
        return "coder"
    return "researcher"

graph.add_conditional_edges(
    START,
    route_to_agent,
    {"coder": "coder", "researcher": "researcher"}
)
```

### Human-in-the-Loop

Interrupt execution for approval:

```python
app = graph.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["tools"]
)
# Resume after approval
app.invoke(None, config)
```

## Learning Resources

1. Start with [examples/README.md](examples/README.md) for hands-on learning
2. Review [SKILL.md](SKILL.md) for detailed implementation patterns
3. Use [references/official-docs-index.md](references/official-docs-index.md) for targeted documentation

## Official Documentation

- [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)
- [LangChain Documentation](https://docs.langchain.com/oss/python/langchain/overview)

## License

This skill is part of the av-skill project and follows the same license terms.
