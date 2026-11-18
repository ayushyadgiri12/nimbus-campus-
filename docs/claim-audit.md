# PART A — CLAIM AUDIT & FACTUAL VERIFICATION REPORT

**Project:** Nimbus Labs — Campus Helpdesk Agent  
**Student:** Ayush Yadgiri | **Roll No:** 150096725098  
**Subject:** AI Tools and Prompt Engineering  
**Audit Date:** November 2026  
**Auditor Verification Standard:** Official Specifications, Public Registries, RFC Index, Academic Indices.

---

### Audit Summary Matrix

| # | Claim Topic | Claimed Statement | Verdict | Authoritative Evidence / Source URL |
|---|-------------|-------------------|---------|--------------------------------------|
| 1 | MCP Foundation & Primitives | Uses JSON-RPC 2.0; standard primitives are tools, resources, and prompts | **TRUE** | [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/) |
| 2 | Persistent Memory Primitive | Spec defines mandatory Persistent Memory Primitive (rev 2025-02-30) | **FALSE** | [MCP Architecture Spec](https://spec.modelcontextprotocol.io/specification/architecture/) |
| 3 | Agent Skills Progressive Disclosure | Uses directory structure with `SKILL.md` and progressive disclosure | **TRUE** | [Agent Skills Specification](https://agentskills.io/specification) |
| 4 | Mandatory skill.config.yaml | Every Agent Skill must include `skill.config.yaml` with `runtime` field | **FALSE** | [Agent Skills Directory Structure](https://agentskills.io/specification#structure) |
| 5 | Git Worktrees Storage Architecture | Linked worktrees share common object database & refs with separate HEADs | **TRUE** | [Git Documentation — git-worktree](https://git-scm.com/docs/git-worktree) |
| 6 | Git Worktree Sync Command | Git CLI includes built-in `git worktree sync --all` command | **FALSE** | [Git Documentation — Subcommands](https://git-scm.com/docs/git-worktree#_commands) |
| 7 | Claude Code Plugin Extensibility | Plugins bundle Skills, slash commands, hooks, subagents & MCP servers | **TRUE** | [Anthropic Claude Code Plugins](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/plugins) |
| 8 | MCP Transport Security Specification | RFC 9999 mandates Ed25519 signing on stdio transport | **FALSE** | [IETF RFC Database](https://www.rfc-editor.org/rfc-index.html) |
| 9 | Duplicate Worktree Branch Checkout | Same branch can be checked out in multiple worktrees by default | **FALSE** | [Git Documentation — git-worktree](https://git-scm.com/docs/git-worktree) |
| 10 | Skill Collapse Phenomenon | Hendricks & Oyelaran (2024) proved >12 skills causes 40% accuracy drop | **UNVERIFIED** | [arXiv](https://arxiv.org/) / [Google Scholar](https://scholar.google.com/) |

---

### Detailed Claim-by-Claim Verification & Correction

#### Claim 1: Model Context Protocol Core Primitives
- **Statement:** The Model Context Protocol (MCP) relies on JSON-RPC 2.0 as its wire format and standardises three core server primitives: tools, resources, and prompts.
- **Status:** **TRUE**
- **Explanation:** The official Model Context Protocol architectural specification explicitly mandates JSON-RPC 2.0 for all message framing across stdio and streamable HTTP/SSE transports. Furthermore, the specification formally defines exactly three primary primitives that servers expose to clients: Tools (model-controlled executable actions), Resources (contextual passive data streams read by the host application), and Prompts (reusable parameterized template prompts).
- **Official Source URL:** https://spec.modelcontextprotocol.io/specification/2024-11-05/architecture/
- **Verification / Access Date:** 2026-11-18

#### Claim 2: Alleged Mandatory Persistent Memory Primitive
- **Statement:** The MCP specification defines a mandatory "Persistent Memory Primitive" introduced in revision 2025-02-30.
- **Status:** **FALSE**
- **Correction:** The MCP specification does not contain a "Persistent Memory Primitive", nor is there any protocol revision dated 2025-02-30 (February 30 is a non-existent calendar date).
- **Explanation:** MCP server state is entirely application-defined; the core specification defines only tools, resources, prompts, and sampling primitives. Furthermore, protocol revision versions follow standard ISO calendar dates (such as `2024-11-05`), making `2025-02-30` both technically and chronologically impossible. Persistent memory in LLM architectures is handled outside MCP core or modeled as standard custom tools/resources.
- **Official Source URL:** https://spec.modelcontextprotocol.io/specification/
- **Verification / Access Date:** 2026-11-18

#### Claim 3: Agent Skills Progressive Disclosure Architecture
- **Statement:** Agent Skills use a filesystem directory structure containing a required `SKILL.md` file with YAML frontmatter and support progressive disclosure.
- **Status:** **TRUE**
- **Explanation:** In open agent skill standards, an Agent Skill is defined as a directory containing a required `SKILL.md` document with valid YAML frontmatter specifying `name` and `description`. Progressive disclosure is the core design philosophy: lightweight metadata is loaded into primary agent context at initialization, while full instructions, reference dictionaries, and deterministic helper scripts are fetched on-demand only when triggers match.
- **Official Source URL:** https://agentskills.io/specification
- **Verification / Access Date:** 2026-11-18

#### Claim 4: Alleged Mandatory skill.config.yaml Runtime Descriptor
- **Statement:** Every Agent Skill must include a `skill.config.yaml` file that declares a `runtime` field (e.g. `python3` or `node`).
- **Status:** **FALSE**
- **Correction:** The Agent Skills specification requires only `SKILL.md` with standard YAML frontmatter; there is no specification requirement for a `skill.config.yaml` file.
- **Explanation:** Agent Skills rely exclusively on the markdown file's YAML frontmatter for declaration and semantic routing. Optional scripts within a skill's directory (such as `scripts/lookup_timetable.py`) are normal executable files invoked via standard system PATH or interpreter shebangs, not orchestrated through a mandatory runtime manifest.
- **Official Source URL:** https://agentskills.io/specification#structure
- **Verification / Access Date:** 2026-11-18

#### Claim 5: Git Linked Worktree Architecture
- **Statement:** Git linked worktrees share a single common object database and refs namespace with the main repository while maintaining separate working trees and HEAD references.
- **Status:** **TRUE**
- **Explanation:** A Git repository initialized with linked worktrees stores all object blobs, trees, tags, and commits in the primary `.git/objects` directory, avoiding repository duplication. Each linked worktree maintains an isolated administrative directory inside `.git/worktrees/<name>/` that holds an independent `HEAD`, `index`, and worktree-specific config, enabling concurrent branch checkouts without data duplication.
- **Official Source URL:** https://git-scm.com/docs/git-worktree
- **Verification / Access Date:** 2026-11-18

#### Claim 6: Alleged Built-In `git worktree sync --all` Command
- **Statement:** Git provides a built-in command `git worktree sync --all` to automatically synchronize worktrees across branches.
- **Status:** **FALSE**
- **Correction:** The `git worktree` command suite contains no `sync` subcommand; valid subcommands are `add`, `list`, `lock`, `move`, `prune`, `remove`, and `unlock`.
- **Explanation:** Git does not provide an automated multi-worktree branch synchronization tool because worktrees are local checkouts with independent working directories. Synchronizing state across branches in Git requires standard fetch, rebase, or merge operations executed individually per branch.
- **Official Source URL:** https://git-scm.com/docs/git-worktree
- **Verification / Access Date:** 2026-11-18

#### Claim 7: Claude Code Plugin Format & Capabilities
- **Statement:** Claude Code plugins can bundle Skills, custom slash commands, hooks (including PreToolUse), subagents, and MCP server configurations in a single distributable bundle.
- **Status:** **TRUE**
- **Explanation:** Claude Code plugin manifests (`plugin.json` or equivalent directory packaging) officially support bundling reusable Agent Skills (`skills/`), custom slash commands (`commands/*.md`), lifecycle event hooks (`PreToolUse`, `PostToolUse`), custom subagent definitions, and local/remote MCP server connection declarations (`.mcp.json` or `mcpServers` configuration).
- **Official Source URL:** https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/plugins
- **Verification / Access Date:** 2026-11-18

#### Claim 8: Alleged RFC 9999 MCP Transport Security Specification
- **Statement:** RFC 9999 specifies Model Context Protocol transport security, mandating Ed25519 cryptographic signatures for all stdio-based communication.
- **Status:** **FALSE**
- **Correction:** RFC 9999 has not been published by the IETF (as of late 2026 RFC numbers have not reached 9999), and MCP transport security is not standardized by an IETF RFC.
- **Explanation:** MCP is an open specification stewarded by Anthropic and the open-source community, not an IETF Internet Standard. Furthermore, stdio transport relies fundamentally on local OS process isolation and process pipe security (POSIX pipes / Windows anonymous pipes), making per-message Ed25519 cryptographic signatures unnecessary for local inter-process communication.
- **Official Source URL:** https://www.rfc-editor.org/rfc-index.html
- **Verification / Access Date:** 2026-11-18

#### Claim 9: Checking Out the Same Branch Across Multiple Worktrees
- **Statement:** By default, Git permits the same local branch to be checked out simultaneously across multiple linked worktrees.
- **Status:** **FALSE**
- **Correction:** Git strictly refuses to allow checking out the same branch in more than one worktree simultaneously by default, exiting with a fatal error.
- **Explanation:** To protect the repository from race conditions, index corruption, and divergent uncommitted state across multiple working directories, Git prohibits multiple checkouts of the same branch ref. Attempting to check out an already checked-out branch yields: `fatal: '<branch>' is already used by worktree at '<path>'`. While an override flag `--ignore-other-worktrees` exists, its use is strongly discouraged.
- **Official Source URL:** https://git-scm.com/docs/git-worktree
- **Verification / Access Date:** 2026-11-18

#### Claim 10: Academic Paper on "Skill Collapse" by Hendricks & Oyelaran
- **Statement:** Hendricks and Oyelaran (2024) demonstrated that loading more than 12 agent skills causes a 40% accuracy drop known as "skill collapse."
- **Status:** **UNVERIFIED**
- **Correction:** There is no verifiable publication by authors named "Hendricks and Oyelaran" in 2024 documenting a "skill collapse" benchmark or 40% performance drop.
- **Explanation:** A rigorous query across computer science academic indices, arXiv, Google Scholar, DBLP, and ACL Anthology reveals no peer-reviewed or preprint paper matching these authors, titles, and exact numerical figures. While context degradation and prompt dilution with excessive in-context tool definitions is a recognized empirical issue in LLM literature, this specific citation appears to be a hallucinated or fabricated academic reference.
- **Official Source URL:** https://scholar.google.com/ and https://arxiv.org/
- **Verification / Access Date:** 2026-11-18
