---
name: langgraph-agent
description: Design, implement, and debug LangGraph agents for building stateful, multi-step workflows with LLMs. Use when creating LangGraph agents, implementing StateGraph workflows, adding memory and persistence, incorporating human-in-the-loop patterns, or implementing complex agent architectures with conditional branching and multi-agent systems.
---

# LangGraph Agent Developer

## Overview

LangGraph is a low-level orchestration framework for building stateful, multi-actor applications with LLMs. It enables you to create cyclical graphs that define agent workflows, with built-in support for persistence, streaming, and human-in-the-loop interactions.

## Core Concepts

### State Management

LangGraph applications revolve around a **State** object that passes between nodes:

```python
from typing_extensions import TypedDict
from typing import Annotated
from operator import add

class State(TypedDict):
    # Single value
    query: str
    # Accumulates across nodes
    messages: Annotated[list, add]
    # Optional values
    context: str | None
```

### Graph Structure

LangGraph uses **StateGraph** to define workflows:

```python
from langgraph.graph import START, END, StateGraph

graph = StateGraph(State)

# Add nodes
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)

# Add edges
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, {
    "continue": "tools",
    "end": END
})
graph.add_edge("tools", "agent")

# Compile and invoke
app = graph.compile()
result = app.invoke({"query": "hello"})
```

### Key Features

- **Durable Execution**: Persist state and resume from checkpoints
- **Human-in-the-Loop**: Interrupt execution for human approval
- **Streaming**: Stream tokens, steps, or graph updates
- **Memory**: Built-in short-term and long-term memory
- **Multi-agent**: Coordinate multiple agents in single workflow

## Workflow

### 1. Design the Agent Architecture

Identify the core components:

**Nodes**: Define what each step does
- Agent nodes (LLM calls)
- Tool nodes (function execution)
- Router nodes (conditional logic)
- Sub-graph nodes (nested workflows)

**Edges**: Define flow control
- Simple edges: unconditional transition
- Conditional edges: routing based on state

**State**: Define shared data
- Input/output schema
- Accumulated data (messages, results)
- Configuration (model params, settings)

### 2. Implement the Graph

Start with a minimal working example:

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
```

### 3. Add Tools (if needed)

Use LangChain's tool integration:

```python
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

@tool
def search(query: str) -> str:
    """Search the web."""
    return f"Results for: {query}"

tools = [search]
tool_node = ToolNode(tools)

# Bind tools to model
def agent(state: State):
    model = ChatAnthropic(model="claude-sonnet-4-5-20250213")
    model_with_tools = model.bind_tools(tools)
    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}
```

### 4. Implement Conditional Routing

Add decision logic with conditional edges:

```python
def should_continue(state: State) -> str:
    messages = state["messages"]
    last_message = messages[-1]

    if last_message.tool_calls:
        return "tools"
    return END

graph.add_conditional_edges(
    "agent",
    should_continue,
    {"tools": "tools", END: END}
)
```

### 5. Add Memory and Persistence

Enable checkpointing for stateful conversations:

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
app = graph.compile(checkpointer=memory)

# Use thread_id for conversation continuity
config = {"configurable": {"thread_id": "conversation-1"}}
result = app.invoke({"messages": [("user", "hello")]}, config)
```

### 6. Implement Human-in-the-Loop

Add interruption points for human approval:

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
app = graph.compile(
    checkpointer=memory,
    interrupt_before=["tools"]  # Pause before executing tools
)

# Resume after human approval
app.invoke(None, config)
```

## Common Patterns

### ReAct Agent

Reason + Act pattern for tool-using agents:

```python
from langgraph.prebuilt import create_react_agent

tools = [search, calculator]
agent = create_react_agent(
    model="claude-sonnet-4-5-20250213",
    tools=tools,
    checkpointer=MemorySaver()
)
```

### Multi-Agent System

Coordinate specialized agents:

```python
from langgraph.graph import StateGraph

# Define sub-agents
researcher = create_research_agent()
coder = create_coder_agent()

# Coordinator
def coordinator(state: State):
    # Route to appropriate agent
    if "code" in state["query"]:
        return "coder"
    return "researcher"

# Build multi-agent graph
graph = StateGraph(State)
graph.add_node("coordinator", coordinator)
graph.add_node("researcher", researcher)
graph.add_node("coder", coder)
graph.add_conditional_edges("coordinator", coordinator)
```

### Sequential Chain

Linear workflow with clear steps:

```python
def step1(state):
    # Process input
    return {"data": transform(state["input"])}

def step2(state):
    # Process output from step1
    return {"result": analyze(state["data"])}

graph = StateGraph(State)
graph.add_node("step1", step1)
graph.add_node("step2", step2)
graph.add_edge(START, "step1")
graph.add_edge("step1", "step2")
graph.add_edge("step2", END)
```

### Router Pattern

Route inputs to different branches:

```python
def route_intent(state: State) -> str:
    query = state["query"].lower()

    if "weather" in query:
        return "weather_agent"
    elif "code" in query:
        return "code_agent"
    else:
        return "general_agent"

graph.add_conditional_edges(
    START,
    route_intent,
    {
        "weather_agent": "weather",
        "code_agent": "code",
        "general_agent": "general"
    }
)
```

## Debugging

### Visualize the Graph

```python
from IPython.display import Image, display

try:
    display(Image(app.get_graph().draw_mermaid_png()))
except Exception:
    print(app.get_graph().print_ascii())
```

### Inspect State

```python
# Get current state
state = app.get_state(config)
print(state.next)    # Next nodes to execute
print(state.values)  # Current state values

# Get state history
for state in app.get_state_history(config):
    print(state.values, state.next)
```

### Stream Execution

```python
# Stream tokens
for chunk in app.stream({"messages": [("user", query)]}, config):
    print(chunk)

# Stream updates
for event in app.stream({"messages": [("user", query)]}, config, stream_mode="updates"):
    print(event)

# Stream debug info
async for event in app.astream_events(
    {"messages": [("user", query)]},
    config,
    version="v1"
):
    print(f"Node: {event['name']}, Type: {event['event']}")
```

## Deployment

### LangGraph Platform (Recommended)

Deploy to LangGraph Cloud for production:

```bash
# Install CLI
pip install langgraph-cli

# Initialize project
langgraph init

# Deploy
langgraph deploy
```

### Self-Hosted

Use FastAPI for custom deployment:

```python
from fastapi import FastAPI
from langgraph.graph import StateGraph

app_api = FastAPI()
graph_app = graph.compile()

@app_api.post("/invoke")
async def invoke(request: dict):
    result = graph_app.invoke(request["state"], request["config"])
    return {"result": result}
```

## Best Practices

1. **Start Simple**: Begin with a basic graph, then add complexity
2. **Type State**: Use TypedDict for clear state schemas
3. **Error Handling**: Wrap LLM calls in try-except blocks
4. **Idempotent Nodes**: Nodes should handle re-execution safely
5. **Separate Concerns**: Keep business logic separate from graph definition
6. **Test Locally**: Use `invoke` for testing before `stream`/`astream`
7. **Monitor**: Use LangSmith for tracing and debugging

## Implementation Rules

- Read `references/official-docs-index.md` for focused documentation links
- Use Python type hints for all State definitions
- Prefer `create_react_agent` for simple tool-using agents
- Use conditional edges for all branching logic
- Always include proper error handling in production code
- Test with streaming to understand execution flow
- Use checkpointing for any long-running or stateful workflow
- Keep nodes small and focused on single responsibilities
- Document complex routing logic in comments

## Task Playbooks

### Create Simple Sequential Agent

1. Define State with input/output fields
2. Create 2-3 processing nodes
3. Chain nodes with simple edges
4. Compile and test with invoke
5. Add streaming if needed

### Build Tool-Using Agent

1. Define tools with type hints and docstrings
2. Create agent node with model.bind_tools()
3. Add ToolNode for tool execution
4. Implement should_continue conditional logic
5. Add checkpointing for conversation memory

### Implement Multi-Agent System

1. Define each agent's purpose and state interface
2. Create individual agent graphs or functions
3. Design coordinator/routing logic
4. Combine agents in parent graph
5. Test routing and communication flows

## References

Use `references/official-docs-index.md` for direct links to official documentation.
