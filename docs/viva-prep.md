# Viva Voce Preparation Guide

**Project:** Nimbus Labs — Campus Helpdesk Agent  
**Student:** Ayush Yadgiri (Roll No: 150096725098)  
**Subject:** AI Tools and Prompt Engineering  

---

### Core Questions & Model Answers

#### Q1: What is the Model Context Protocol (MCP) and how does it work?
**Answer:** MCP is an open standard that enables AI models to connect securely to external tools and data sources. It uses **JSON-RPC 2.0** as its wire format over transports like **stdio** (standard in/out for local processes) or **SSE/HTTP** (for remote servers). An MCP server exposes three core primitives: **Tools** (actions the model can execute), **Resources** (data/files the model can read), and **Prompts** (predefined interaction templates).

#### Q2: What is the difference between an Agent Skill and an MCP Tool?
**Answer:**
- An **Agent Skill** (`skills/`) provides procedural intelligence and guidelines in-context (the agent's internal playbook). It tells the agent *how to think*, how to validate parameters, and how to refuse hallucinations using progressive disclosure.
- An **MCP Tool** (`mcp-server/`) executes outside the LLM context in a separate server process. It handles external state, database queries, and live system computations.

#### Q3: What is "Progressive Disclosure" in Agent Skills?
**Answer:** Progressive disclosure is an architectural pattern where an agent only loads high-level metadata (name and trigger description) during initial system setup. The agent does not read the full instructions, column dictionaries, or edge cases until user intent matches the trigger. This prevents context window bloat, reduces token costs, and avoids instruction confusion.

#### Q4: How does Git Worktrees work and why are they valuable for AI agents?
**Answer:** Git worktrees allow multiple linked working directories to share a single `.git` repository and object database. For AI agents, worktrees allow concurrent branching, code generation, and test execution without branch checkout collisions or index corruption. Git prevents checking out the same branch in multiple worktrees to avoid race conditions and uncommitted state divergence.

#### Q5: What security risks exist with MCP tools and AI shell hooks?
**Answer:**
1. **Tool Description Poisoning:** Attackers can inject prompt injection payloads into tool descriptions, tricking the LLM into exfiltrating conversation history.
2. **PreToolUse Hook Bypass:** Naive regex matchers or unexpanded shell variables (like literal `~`) can allow an agent to inadvertently write to sensitive directories (`.ssh`, `.bashrc`). Hooks must validate absolute normalized paths and fail closed.

#### Q6: What did your audit reveal about `@nimbus/mcp-skill-bridge` and RFC 9999?
**Answer:**
- `@nimbus/mcp-skill-bridge@2.3` does not exist on the public npm registry (`HTTP 404 Not Found`). It is an unverified fictional dependency.
- RFC 9999 has not been published by the IETF. MCP is an open industry protocol stewarded by Anthropic, not an IETF standard, and stdio relies on local OS pipe security rather than Ed25519 signatures.
