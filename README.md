# Nimbus Labs — Campus Helpdesk Agent

**Student Name:** Ayush Yadgiri  
**Roll Number:** 150096725098  
**Subject:** AI Tools and Prompt Engineering  
**Maximum Marks:** 100  
**Platform:** macOS, VS Code  

---

## Executive Summary

The **Nimbus Labs Campus Helpdesk Agent** is a production-grade, highly audited AI agent architecture designed to assist university students with academic schedules, fee inquiries, and campus policy navigation.

This repository fulfills all six parts (A–F) of the semester assignment:
- **Part A:** Rigorous Claim Audit of 10 industry and academic claims with verified official citations.
- **Part B:** Deterministic `timetable-helper` Agent Skill with YAML frontmatter, progressive disclosure, edge-case handling, and fabrication refusal tests.
- **Part C:** Claude Code plugin `campus-helpdesk` bundling skills, `/campus-status` slash command, a safe `PreToolUse` shell hook, and threat modeling.
- **Part D:** Python MCP Server built on the official `modelcontextprotocol` SDK (v2.3.0 `MCPServer`), exposing two tools, one resource, and annotated JSON-RPC traces.
- **Part E:** Git worktrees architecture with 3 linked worktrees, simulated and resolved merge conflict, real terminal outputs, and architectural analysis.
- **Part F:** Comprehensive prompt log, 300-word engineering reflection, sources index, and viva voce preparation guide.

---

## Repository Structure

```text
campus-helpdesk-agent/
├── README.md                      # Comprehensive project guide and macOS instructions
├── .gitignore                     # Git ignore rules (.venv, worktrees, cache)
├── data/
│   └── timetable.csv              # Fictional campus class schedules (CS2024A, CS2024B, EC2024A)
├── skills/
│   └── timetable-helper/          # Timetable Agent Skill
│       ├── SKILL.md               # Progressive disclosure specification with YAML frontmatter
│       ├── references/
│       │   ├── column-dictionary.md
│       │   └── edge-cases.md      # Refusal policy EC-05 and edge case rules
│       └── scripts/
│           └── lookup_timetable.py # Deterministic lookup script with input validation
├── plugin/                        # Claude Code Plugin bundle
│   ├── plugin.json                # Plugin manifest specification
│   ├── commands/
│   │   └── campus-status.md       # Custom /campus-status slash command
│   ├── hooks/
│   │   └── protect-paths.sh       # PreToolUse hook protecting sensitive directories
│   └── skills/                    # Bundled skill mirror for plugin distribution
├── mcp-server/                    # Model Context Protocol Server
│   ├── server.py                  # Python MCP Server (mcp.server.mcpserver.MCPServer)
│   ├── requirements.txt           # Python dependencies
│   └── README.md                  # Server docs with annotated JSON-RPC traces
├── tests/                         # Full automated test suites (26 tests total)
│   ├── test_timetable.py          # 10 tests: 3 positive, 2 negative, 1 adversarial, 4 edge
│   ├── test_skill_integration.py  # Worktree feature branch integration tests
│   └── test_mcp_server.py         # 16 tests: tools, resources, error dictionaries, validation
├── docs/                          # Detailed technical documentation
│   ├── claim-audit.md             # Part A Claim Audit with official citations
│   ├── git-worktrees-report.md    # Part E Worktrees log and analysis
│   ├── prompt-log.md              # Part F Iterative engineering prompt entries
│   ├── reflection.md              # Part F Architectural roles reflection
│   └── sources.md                 # Primary official sources index
└── screenshots/
    └── checklist.md               # Step-by-step genuine evidence capture checklist
```

---

## macOS Quick Start Instructions

### 1. Prerequisites
- macOS (Apple Silicon or Intel)
- Python 3.10+ (Python 3.14 recommended via Homebrew: `/opt/homebrew/bin/python3.14`)
- Git & Bash

### 2. Setting Up the Virtual Environment
```bash
cd campus-helpdesk-agent/

# Create venv with Python 3.14 (or python3 if >= 3.10)
/opt/homebrew/bin/python3.14 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r mcp-server/requirements.txt
```

### 3. Running All Automated Tests
```bash
# Activate venv
source .venv/bin/activate

# 1. Run Timetable Skill tests (10 tests: positive, negative, adversarial)
python3 tests/test_timetable.py

# 2. Run MCP Server business logic tests (16 tests)
python3 tests/test_mcp_server.py
```
*Expected Result:* All tests pass (`OK`).

### 4. Running the MCP Server
```bash
source .venv/bin/activate
python3 mcp-server/server.py
```
*(The server runs over stdio waiting for JSON-RPC messages from MCP clients such as Claude Desktop or MCP Inspector).*

To inspect visually using the official inspector:
```bash
npx @modelcontextprotocol/inspector python3 mcp-server/server.py
```

### 5. Inspecting Git Worktrees & Commit History
```bash
git worktree list
git log --oneline --graph --decorate --all -n 12
```

---

## Academic Integrity & Verification Guarantee

All claims and dependencies have been audited against primary official sources:
- `@nimbus/mcp-skill-bridge@2.3`: **Verified non-existent (HTTP 404)** on the public npm registry.
- `git worktree sync --all`: **Verified non-existent** in Git core specification.
- Persistent Memory Primitive (2025-02-30): **Verified false/invalid**.
- RFC 9999 Ed25519 stdio: **Verified non-existent** in IETF index.
- "Skill collapse" paper: **Verified unverified** in academic preprint repositories.
