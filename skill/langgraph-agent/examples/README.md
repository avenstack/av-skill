# LangGraph Agent Examples

This directory contains example code demonstrating various LangGraph patterns and implementations.

## Examples

### 1. Sequential Chain (`01_sequential_chain.py`)

Demonstrates a simple sequential workflow where data flows through a series of processing steps.

**Key concepts:**
- StateGraph definition
- Adding nodes to the graph
- Connecting nodes with edges
- Basic state management

**Run:**
```bash
python 01_sequential_chain.py
```

### 2. ReAct Agent (`02_react_agent.py`)

Implements a ReAct (Reason + Act) agent that can use tools to answer questions and perform actions.

**Key concepts:**
- Tool definition with `@tool` decorator
- ToolNode for tool execution
- Conditional routing based on LLM responses
- Agent-tool orchestration

**Run:**
```bash
# Set ANTHROPIC_API_KEY environment variable first
export ANTHROPIC_API_KEY="your-api-key"
python 02_react_agent.py
```

### 3. Memory and Persistence (`03_memory_persistence.py`)

Shows how to add conversation memory and state persistence to maintain context across interactions.

**Key concepts:**
- MemorySaver for in-memory checkpointing
- Thread-based conversation tracking
- Multi-turn conversations
- State history retrieval

**Run:**
```bash
export ANTHROPIC_API_KEY="your-api-key"
python 03_memory_persistence.py
```

### 4. Human-in-the-Loop (`04_human_in_the_loop.py`)

Demonstrates interrupting execution for human approval before continuing with sensitive operations.

**Key concepts:**
- Interrupt points in graph execution
- State inspection
- Resume after approval
- Approval workflows

**Run:**
```bash
export ANTHROPIC_API_KEY="your-api-key"
python 04_human_in_the_loop.py
```

### 5. Multi-Agent System (`05_multi_agent.py`)

Shows how to coordinate multiple specialized agents in a single workflow using a router pattern.

**Key concepts:**
- Specialized agent nodes
- Conditional routing based on query content
- Agent coordination
- Enum-based agent types

**Run:**
```bash
export ANTHROPIC_API_KEY="your-api-key"
python 05_multi_agent.py
```

## Prerequisites

Install the required dependencies:

```bash
pip install langgraph langchain-anthropic langchain-core
```

Set up your Anthropic API key:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Learning Path

1. Start with `01_sequential_chain.py` to understand basic graph structure
2. Move to `02_react_agent.py` to learn about tools and routing
3. Try `03_memory_persistence.py` to add stateful conversations
4. Explore `04_human_in_the_loop.py` for interactive workflows
5. Build `05_multi_agent.py` for complex agent coordination

## Next Steps

After mastering these examples, explore:

- Custom checkpointer implementations (Postgres, Redis, etc.)
- Streaming responses with `astream()` and `astream_events()`
- Subgraphs for nested agent workflows
- LangSmith integration for tracing and debugging
- Deployment with LangGraph Cloud or self-hosted solutions

See [official-docs-index.md](../references/official-docs-index.md) for more learning resources.
