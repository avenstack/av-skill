# AV-Skill

Agent Skills Collection - A collection of specialized skills for AI agent development and automation.

## Skills

### [langgraph-agent](skill/langgraph-agent/)

Design, implement, and debug LangGraph agents for building stateful, multi-step workflows with LLMs.

**Features:**
- Build stateful agents with LangGraph's StateGraph
- Implement ReAct (Reason + Act) patterns for tool-using agents
- Add memory and persistence for conversation continuity
- Create human-in-the-loop workflows with approval steps
- Coordinate multi-agent systems with specialized agents
- Stream responses and debug with LangSmith integration

**Use Cases:**
- Creating conversational AI agents with memory
- Building multi-step workflows with conditional logic
- Implementing tool-using agents that can call external APIs
- Designing approval workflows for sensitive operations
- Coordinating multiple specialized agents in a single system

**Documentation:**
- [Skill Documentation](skill/langgraph-agent/SKILL.md)
- [Examples](skill/langgraph-agent/examples/)
- [Official Docs Index](skill/langgraph-agent/references/official-docs-index.md)

### [joplin-plugin-writer](skill/joplin-plugin-writer/)

Write, refactor, and debug Joplin plugins for desktop/mobile using the official Joplin plugin architecture, API, and manifest rules.

**Use Cases:**
- Create new Joplin plugins from scratch
- Add features to existing plugins
- Build CodeMirror/editor extensions
- Fix plugin loading/runtime errors
- Prepare manifest/package output

## Getting Started

Each skill is self-contained with its own documentation and examples. Navigate to the specific skill directory to get started:

```bash
cd skill/<skill-name>
```

See the individual skill's README.md for detailed usage instructions.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
