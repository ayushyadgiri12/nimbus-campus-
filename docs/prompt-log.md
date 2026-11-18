# Nimbus Labs Campus Helpdesk — Engineering Prompt Log

**Project:** Nimbus Labs — Campus Helpdesk Agent  
**Student:** Ayush Yadgiri (Roll No: 150096725098)  
**Subject:** AI Tools and Prompt Engineering  
**Methodology:** Iterative prompt engineering with rigorous verification against primary documentation. No fabricated conversation transcripts.

---

### Prompt Entry 1: Agent Skill Architecture & Refusal Guarantees
* **AI Tool / Model:** Claude 3.5 Sonnet / Antigravity Agent
* **Exact Prompt:**
  > "Design the `timetable-helper` Skill structure with progressive disclosure. The skill must query class schedules deterministically from a fictional CSV and strictly refuse to invent or hallucinate classes that do not exist. Write the lookup script in Python."
* **Summary of Output:**
  The model generated `skills/timetable-helper/SKILL.md` along with reference files and a Python script using `csv.DictReader` that filters rows matching batch and day.
* **What Was Changed or Rejected and Why:**
  1. *Python Compatibility Issue:* The model originally utilized Python 3.10+ union operator type hints (`dict | None`) directly in functions intended to execute on macOS system Python (`3.9.6`). The script crashed during initial runs. I edited the script to use standard `typing.Optional[dict]` and backwards-compatible type annotations.
  2. *Refusal Hardening:* The model initially returned an empty list when an invented class was queried. I rejected this passive behavior and added an explicit `EC-05` fabrication refusal branch in `lookup_timetable.py` that emits an unambiguous warning and refuses to generate plausible-sounding room or teacher details.
* **How the Claim Was Verified:**
  Executed `tests/test_timetable.py` containing test case `test_adversarial_invented_subject` querying non-existent class "Quantum Computing". Verified that the script output explicitly contained "not found" and "refuses to fabricate" while producing zero hallucinations.

---

### Prompt Entry 2: Claude Code Plugin Manifest & Hook Configuration
* **AI Tool / Model:** Claude 3.5 Sonnet / Antigravity Agent
* **Exact Prompt:**
  > "Create a valid Claude Code plugin manifest `plugin.json` for campus-helpdesk that bundles the timetable-helper skill, adds a `/campus-status` slash command, configures a PreToolUse hook blocking sensitive paths, and wires the MCP server via stdio."
* **Summary of Output:**
  The model produced a `plugin.json` manifest specifying schema fields for skills, slash commands, lifecycle hooks (`PreToolUse` with regex matcher), and `mcpServers`.
* **What Was Changed or Rejected and Why:**
  1. *Hook Regex Matcher:* The model initially used a loose regex `"write|edit"` which failed to capture case-sensitive Anthropic tool names like `MultiEdit` or custom filesystem tools. I refined the matcher to `"Write|Edit|MultiEdit"`.
  2. *Hook Path Expansion:* The shell hook initially checked `~/.ssh` literally as a string. Because standard JSON payloads from tool calls contain literal absolute paths, tilde expansion did not match. In branch `bugfix/hook-path`, this was fixed to evaluate `${HOME}` explicitly.
* **How the Claim Was Verified:**
  Verified against the official Anthropic Claude Code plugin specification (`https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/plugins`) confirming schema names, lifecycle hook events, and command registration conventions.

---

### Prompt Entry 3: MCP Server Python SDK 2.x Migration
* **AI Tool / Model:** Claude 3.5 Sonnet / Antigravity Agent
* **Exact Prompt:**
  > "Implement the campus-helpdesk MCP server in Python exposing `get_timetable`, `get_fee_status`, and `hostel://rules` resource using the official `modelcontextprotocol` package."
* **Summary of Output:**
  The model generated `server.py` using `from mcp.server.fastmcp import FastMCP` with `@mcp.tool()` and `@mcp.resource()` decorators.
* **What Was Changed or Rejected and Why:**
  1. *FastMCP Deprecation in SDK v2:* When running `pip install "mcp[cli]"` in the Python 3.14 virtual environment, `mcp==2.3.0` was installed. In v2.x, importing `mcp.server.fastmcp` throws a `ModuleNotFoundError` because `FastMCP` was refactored and renamed to `MCPServer` (`mcp.server.mcpserver.MCPServer`).
  2. *Refactoring:* I updated `server.py` to import `MCPServer`, retained the `@mcp.tool()` and `@mcp.resource()` interfaces, and cleanly separated pure Python business logic functions so they could be directly imported and tested by `tests/test_mcp_server.py`.
* **How the Claim Was Verified:**
  Ran `tests/test_mcp_server.py` against the updated server. All 16 unit tests passed in 0.000s without requiring an active JSON-RPC daemon. Checked official SDK migration guide at `https://py.sdk.modelcontextprotocol.io/v2/migration/`.

---

### Prompt Entry 4: npm Public Registry Verification of `@nimbus/mcp-skill-bridge`
* **AI Tool / Model:** Claude 3.5 Sonnet / Antigravity Agent
* **Exact Prompt:**
  > "Check whether npm package `@nimbus/mcp-skill-bridge` version 2.3 exists and write code depending on it."
* **Summary of Output:**
  The model initially proposed adding `@nimbus/mcp-skill-bridge` to the plugin's package configuration assuming it was an official bridge library.
* **What Was Changed or Rejected and Why:**
  *Rejection of Unverified Dependency:* I rejected adding any dependency on this package. In accordance with the academic integrity policy, I executed `npm view @nimbus/mcp-skill-bridge` against the live npm registry. The query returned `npm error 404 Not Found`. The package does not exist publicly. I marked the claim UNVERIFIED and documented that no real-world system can depend on it.
* **How the Claim Was Verified:**
  Executed terminal command:
  ```bash
  npm view @nimbus/mcp-skill-bridge 2>&1
  # Output: npm error code E404
  # Output: npm error 404 Not Found - GET https://registry.npmjs.org/@nimbus%2fmcp-skill-bridge - Not found
  ```

---

### Prompt Entry 5: Git Worktree Concurrent Checkout & Conflict Simulation
* **AI Tool / Model:** Claude 3.5 Sonnet / Antigravity Agent
* **Exact Prompt:**
  > "Provide instructions to check out the same Git branch in two worktrees simultaneously, and demonstrate merging two worktree branches."
* **Summary of Output:**
  The model suggested checking out `feature/skill-tests` in both worktrees and suggested running `git worktree sync --all`.
* **What Was Changed or Rejected and Why:**
  1. *Factual Correction on Git Worktrees:* The suggestion to checkout the same branch across worktrees was rejected because Git explicitly blocks this to prevent index corruption. I ran the command to prove Git's fatal error: `fatal: 'feature/skill-tests' is already used by worktree at...`.
  2. *Rejection of `git worktree sync`:* The model's mention of a `sync` subcommand was rejected as non-existent in the Git specification.
  3. *Real Conflict Resolution:* Instead, I orchestrated three linked worktrees (`feature/skill-tests`, `feature/mcp-server`, `bugfix/hook-path`), introduced conflicting changes to `plugin/plugin.json`, performed a merge causing a real merge conflict, resolved it manually, and generated a real commit graph.
* **How the Claim Was Verified:**
  Executed real terminal commands `git worktree add -b ...`, `git merge`, and `git log --graph --oneline --decorate --all`. Real terminal output was captured directly into the assignment documentation.
