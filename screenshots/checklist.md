# Evidence & Real Screenshot Checklist

**Student:** Ayush Yadgiri (Roll No: 150096725098)  
**Subject:** AI Tools and Prompt Engineering  
**Academic Integrity Note:** In strict compliance with the assignment instructions, no fake screenshots, fabricated terminals, or mocked UI dialogues have been generated. Below is the exact step-by-step checklist of genuine terminal commands and UI windows for you to capture on your Mac.

---

### Screenshot 1: Timetable Lookup & Adversarial Refusal Test
- **File to Save:** `screenshots/screenshot-01-timetable-tests.png`
- **What to Display:** A macOS Terminal or VS Code integrated terminal showing the execution of `test_timetable.py` with all 10 unit tests passing, particularly highlighting `test_adversarial_invented_subject`.
- **Command to Run:**
  ```bash
  cd /Users/ayushyadgiri/.gemini/antigravity/scratch/campus-helpdesk-agent
  python3 tests/test_timetable.py
  ```
- **Key Evidence to Ensure Visible:**
  - `A1: 'Quantum Computing' does not exist in the CSV for CS2024A. ... ok`
  - `Ran 10 tests in 0.317s`
  - `OK`

---

### Screenshot 2: MCP Server Unit Tests
- **File to Save:** `screenshots/screenshot-02-mcp-tests.png`
- **What to Display:** Terminal output showing the 16 MCP server tests passing in the Python virtual environment.
- **Command to Run:**
  ```bash
  cd /Users/ayushyadgiri/.gemini/antigravity/scratch/campus-helpdesk-agent
  source .venv/bin/activate
  python3 tests/test_mcp_server.py
  ```
- **Key Evidence to Ensure Visible:**
  - `[INFO] MCP server imported successfully. Running tests...`
  - All 16 tests ending in `ok`
  - `Ran 16 tests in 0.000s — OK`

---

### Screenshot 3: Git Worktrees List & Merge History Graph
- **File to Save:** `screenshots/screenshot-03-git-worktrees-graph.png`
- **What to Display:** Terminal showing `git worktree list` displaying all 3 linked worktrees, followed by the ASCII branch merge graph.
- **Command to Run:**
  ```bash
  cd /Users/ayushyadgiri/.gemini/antigravity/scratch/campus-helpdesk-agent
  git worktree list
  echo ""
  git log --oneline --graph --decorate --all -n 12
  ```
- **Key Evidence to Ensure Visible:**
  - 4 active worktree rows: `main`, `bugfix-hook-path`, `feature-mcp-server`, `feature-skill-tests`.
  - The branch merge diagram showing merge commit `b9ac550` and `b5d568f`.

---

### Screenshot 4: Public npm Verification for `@nimbus/mcp-skill-bridge`
- **File to Save:** `screenshots/screenshot-04-npm-404-verification.png`
- **What to Display:** Terminal showing the live npm registry query proving the package does not exist.
- **Command to Run:**
  ```bash
  npm view @nimbus/mcp-skill-bridge
  ```
- **Key Evidence to Ensure Visible:**
  - `npm error 404 Not Found - GET https://registry.npmjs.org/@nimbus%2fmcp-skill-bridge - Not found`
  - Confirms non-existence of Claim 8 / Part D unverified dependency.

---

### Screenshot 5: MCP Inspector UI (Optional Bonus)
- **File to Save:** `screenshots/screenshot-05-mcp-inspector.png`
- **What to Display:** Chrome / Safari browser displaying MCP Inspector connected to `server.py` over stdio.
- **Command to Run:**
  ```bash
  cd /Users/ayushyadgiri/.gemini/antigravity/scratch/campus-helpdesk-agent
  source .venv/bin/activate
  npx @modelcontextprotocol/inspector python3 mcp-server/server.py
  ```
  *Open http://localhost:5173 in browser, click "Tools" -> "mcp_get_timetable" -> run.*
