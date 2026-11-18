# Part F — Engineering Reflection: Architectural Roles & Delegation Boundaries

**Project:** Nimbus Labs — Campus Helpdesk Agent  
**Student:** Ayush Yadgiri (Roll No: 150096725098)  
**Subject:** AI Tools and Prompt Engineering  

---

### Architectural Roles: Skills, Plugins, MCP, and Git Worktrees

In modern autonomous software engineering, building reliable AI systems requires coordinating four distinct layers of abstraction: **Agent Skills**, **Plugins**, the **Model Context Protocol (MCP)**, and **Git Worktrees**.

1. **Agent Skills (`skills/`):** Provide procedural and contextual intelligence. An Agent Skill is essentially the agent’s internal "playbook." Through progressive disclosure, a skill injects domain rules, edge-case guidance, and validation policies into the LLM context only when triggered. It guides the model on *how* to reason, validate, and invoke deterministic scripts without polluting general context.
2. **Plugins (`plugin/`):** Represent the distribution and packaging unit. A plugin bundles skills, user-facing slash commands (`/campus-status`), lifecycle security hooks (`PreToolUse`), and MCP server connections into a single version-controlled manifest (`plugin.json`). While skills teach the agent what to do, plugins package these capabilities into the user’s development environment.
3. **Model Context Protocol (MCP):** Acts as the external execution and integration bridge. MCP provides a standardized JSON-RPC 2.0 interface connecting the agent to local or remote runtime services. It exposes live tools (`get_timetable`, `get_fee_status`) and passive resources (`hostel://rules`). Crucially, MCP isolates execution: backend services run in their own process sandbox, exposing clean schema-validated inputs to the agent.
4. **Git Worktrees:** Solve the developer isolation problem in agentic workflows. When an agent experiments, executes test suites, or generates multi-branch features, linked worktrees provide dedicated physical working directories sharing a single object database. This allows concurrent agent operations without branch switching collisions or index corruption.

---

### Decision Framework: When to Choose an Agent Skill vs. an MCP Tool

| Requirement Dimension | Choose an Agent Skill | Choose an MCP Tool |
|-----------------------|----------------------|--------------------|
| **Primary Purpose** | Guiding reasoning, interpreting domain logic, enforcing refusal policies. | Executing live computations, fetching dynamic data, querying databases/APIs. |
| **Execution Context** | Executes in-context within the LLM conversation stream or local CLI shell. | Executes out-of-process in an isolated server daemon. |
| **Data Dynamicness** | Static or semi-static rules, local datasets (e.g. `data/timetable.csv`). | Live transactional state (e.g. live fee balance, real-time seat availability). |
| **Security Surface** | Subject to prompt injection and context poisoning. | Subject to tool parameter tampering and command execution boundaries. |

**Rule of Thumb:** If the agent needs to know *how to think, what policies to follow, or how to refuse fabrication*, write an **Agent Skill**. If the agent needs to *query external systems, run privileged processes, or read live state*, build an **MCP Tool**.

---

### Critical Boundaries: Actions That Must Never Be Delegated Without Human Review

Autonomous AI agents possess extraordinary velocity but lack contextual accountability. The following classes of actions must **never** be executed autonomously without human confirmation:

1. **Destructive Filesystem Operations:** Overwriting or modifying host system files, shell configuration files (`~/.zshrc`, `~/.bashrc`), SSH keys, AWS credentials, or system paths (`/etc/`, `/System/`). Our `protect-paths.sh` `PreToolUse` hook demonstrates automated gating, but human confirmation remains the gold standard.
2. **Automated Git Branch Merging & Remote Pushes:** Merging branches across worktrees or pushing directly to shared remotes (`main`, `production`) must never be delegated blindly. AI merge resolution frequently favors syntactic compatibility over business logic invariants.
3. **Financial or Disciplinary State Changes:** Processing fee refunds, changing student academic statuses, or imposing hostel disciplinary actions. In our campus helpdesk, the agent may *read* fee status via MCP (`get_fee_status`), but must never possess a tool to modify student balances without authenticated human approval.
4. **External Credential & Secret Management:** Minting API tokens, altering database permissions, or transmitting credentials over unverified protocols.
