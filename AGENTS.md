# Agent Instructions & Memory Bank

Welcome, Agent! This repository uses a **Memory Bank** to maintain state, context, and decisions across different development sessions and agent invocations.

## Memory Bank Directory Structure

All context files are stored under the `.memory_bank/` directory:

- **[productContext.md](.memory_bank/productContext.md)**: Describes the product domain, core features, and user goals.
- **[systemPatterns.md](.memory_bank/systemPatterns.md)**: Explains architectural patterns, design decisions, and code structure.
- **[techContext.md](.memory_bank/techContext.md)**: Contains details on dependencies, setup commands, and technical tools.
- **[activeContext.md](.memory_bank/activeContext.md)**: Reflects the active focus, current tasks, and recent challenges.

## Rules for Agents

Whenever you start a task in this repository, you must:
1. **Read the Memory Bank**: Read `activeContext.md`, `systemPatterns.md`, and `progress.md` before making any code modifications.
2. **Respect the Constraints**: Adhere to established styling and integration patterns (such as standard Tailwind UI, default system fonts, and the Jinja2 + Vue 3 delimiter configurations).
3. **Keep the Memory Bank updated**: As you make changes and progress on tasks, update the files in `.memory_bank/` so subsequent agents are fully aware of what has changed.
