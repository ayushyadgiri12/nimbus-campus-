# Nimbus Labs Campus Helpdesk — Official Sources and Citation Index

**Author:** Ayush Yadgiri (Roll No: 150096725098)  
**Subject:** AI Tools and Prompt Engineering  
**Standard:** Primary official documentation only. No blog posts or unverified secondary forums cited.

---

### 1. Model Context Protocol (MCP)
1. **Model Context Protocol Specification (Architecture & Core Primitives)**  
   - *URL:* https://spec.modelcontextprotocol.io/specification/architecture/  
   - *Access Date:* 2026-11-18  
   - *Relevance:* Authoritative verification of JSON-RPC 2.0 wire format, three standard server primitives (tools, resources, prompts), and lifecycle capability negotiation.
2. **Model Context Protocol Python SDK Repository & Releases**  
   - *URL:* https://github.com/modelcontextprotocol/python-sdk  
   - *Documentation:* https://py.sdk.modelcontextprotocol.io/  
   - *Access Date:* 2026-11-18  
   - *Relevance:* Verification of Python SDK v2.x architecture (`MCPServer` in `mcp.server.mcpserver`), stdio transport execution, and deprecation of v1 `FastMCP` namespace.
3. **npm Official Public Registry**  
   - *URL:* https://registry.npmjs.org/  
   - *Access Date:* 2026-11-18  
   - *Relevance:* Direct query of `@nimbus/mcp-skill-bridge@2.3` verifying HTTP 404 (package does not exist publicly).

### 2. Agent Skills Standards
4. **Agent Skills Open Specification**  
   - *URL:* https://agentskills.io/specification  
   - *Access Date:* 2026-11-18  
   - *Relevance:* Authoritative specification of the `SKILL.md` format, progressive disclosure design pattern, YAML frontmatter syntax (`name`, `description`), and absence of mandatory `skill.config.yaml`.

### 3. Claude Code & Agent Plugin Ecosystem
5. **Anthropic Claude Code Plugin Documentation**  
   - *URL:* https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/plugins  
   - *Access Date:* 2026-11-18  
   - *Relevance:* Authoritative format for `plugin.json`, custom slash command registration, hook lifecycle events (`PreToolUse`), tool matcher regex, and local marketplace installation steps.

### 4. Git Version Control System
6. **Git Worktree Reference Documentation**  
   - *URL:* https://git-scm.com/docs/git-worktree  
   - *Access Date:* 2026-11-18  
   - *Relevance:* Authoritative verification of shared object database (`.git/objects`), administrative directory per worktree (`.git/worktrees/<name>/`), absence of `sync --all` subcommand, and refusal to check out identical branches across worktrees.
7. **Git Merge Reference Documentation**  
   - *URL:* https://git-scm.com/docs/git-merge  
   - *Access Date:* 2026-11-18  
   - *Relevance:* Three-way merge mechanics, conflict marker conventions (`<<<<<<<`, `=======`, `>>>>>>>`), and manual conflict resolution workflows.

### 5. Standards & Academic Repositories
8. **IETF RFC Index (Internet Engineering Task Force)**  
   - *URL:* https://www.rfc-editor.org/rfc-index.html  
   - *Access Date:* 2026-11-18  
   - *Relevance:* Factual verification that RFC 9999 has not been allocated or published by the IETF.
9. **arXiv.org Open-Access Cornell Archive**  
   - *URL:* https://arxiv.org/  
   - *Access Date:* 2026-11-18  
   - *Relevance:* Search across computer science preprints verifying that the alleged publication "Hendricks and Oyelaran (2024)" on skill collapse is unverified / fabricated.
