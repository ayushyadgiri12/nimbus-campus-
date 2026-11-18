# Part E — Git Worktrees Real Execution Log & Technical Analysis

**Project:** Nimbus Labs — Campus Helpdesk Agent  
**Student:** Ayush Yadgiri (Roll No: 150096725098)  
**Verification:** All commands recorded below were executed in real macOS terminal sessions inside `/Users/ayushyadgiri/.gemini/antigravity/scratch/campus-helpdesk-agent`.

---

### 1. Terminal Log: Creating Three Linked Worktrees

```bash
$ mkdir -p ../worktrees
$ git worktree add -b feature/skill-tests ../worktrees/feature-skill-tests
Preparing worktree (new branch 'feature/skill-tests')
HEAD is now at 7e58639 feat: initial commit — Nimbus Labs Campus Helpdesk Agent

$ git worktree add -b feature/mcp-server ../worktrees/feature-mcp-server
Preparing worktree (new branch 'feature/mcp-server')
HEAD is now at 7e58639 feat: initial commit — Nimbus Labs Campus Helpdesk Agent

$ git worktree add -b bugfix/hook-path ../worktrees/bugfix-hook-path
Preparing worktree (new branch 'bugfix/hook-path')
HEAD is now at 7e58639 feat: initial commit — Nimbus Labs Campus Helpdesk Agent
```

### 2. Terminal Log: `git worktree list`

```bash
$ git worktree list
/Users/ayushyadgiri/.gemini/antigravity/scratch/campus-helpdesk-agent         b5d568f [main]
/Users/ayushyadgiri/.gemini/antigravity/scratch/worktrees/bugfix-hook-path    cef1bf7 [bugfix/hook-path]
/Users/ayushyadgiri/.gemini/antigravity/scratch/worktrees/feature-mcp-server  17f0832 [feature/mcp-server]
/Users/ayushyadgiri/.gemini/antigravity/scratch/worktrees/feature-skill-tests 6760015 [feature/skill-tests]
```

### 3. Worktree-Specific Changes

1. **`feature/skill-tests`:**
   - Created `tests/test_skill_integration.py` containing integration test suites for EC2024A schedule lookups and lab session types.
   - Bumped `plugin/plugin.json` version to `1.1.0`.
   - Commit: `ce50719` and `6760015`.

2. **`feature/mcp-server`:**
   - Authored comprehensive `mcp-server/README.md` with JSON-RPC traces, capability negotiation analysis, and security considerations.
   - Bumped `plugin/plugin.json` version to `1.0.1`.
   - Commit: `4e22d5a` and `17f0832`.

3. **`bugfix/hook-path`:**
   - Modified `plugin/hooks/protect-paths.sh` to properly expand `${HOME}` environment variables rather than testing literal `~` strings. Added shell profile scripts (`.zshrc`, `.bashrc`) to blocked paths.
   - Commit: `cef1bf7`.

### 4. Terminal Log: Merge Conflict & Resolution

```bash
$ git merge feature/mcp-server --no-ff -m "merge: feature/mcp-server into main"
Merge made by the 'ort' strategy.
 mcp-server/README.md | 226 +++++++++++++++++++++++++++++++++++++++++++++++++++
 plugin/plugin.json   |   2 +-
 2 files changed, 227 insertions(+), 1 deletion(-)
 create mode 100644 mcp-server/README.md

$ git merge feature/skill-tests
Auto-merging plugin/plugin.json
CONFLICT (content): Merge conflict in plugin/plugin.json
Automatic merge failed; fix conflicts and then commit the result.
```

#### Conflict Markers in `plugin/plugin.json`:
```json
{
  "name": "campus-helpdesk",
<<<<<<< HEAD
  "version": "1.0.1",
=======
  "version": "1.1.0",
>>>>>>> feature/skill-tests
  "description": "Nimbus Labs Campus Helpdesk Plugin..."
```

#### Manual Resolution:
The conflict was resolved by choosing the superset minor release `"1.1.0"`, staging the file with `git add plugin/plugin.json`, and committing the merge result:

```bash
$ git add plugin/plugin.json
$ git commit -m "merge: resolve merge conflict between feature/mcp-server and feature/skill-tests (selected v1.1.0)"
[main b9ac550] merge: resolve merge conflict between feature/mcp-server and feature/skill-tests (selected v1.1.0)
```

Finally, `bugfix/hook-path` was merged cleanly:
```bash
$ git merge bugfix/hook-path --no-ff -m "merge: merge bugfix/hook-path into main"
Merge made by the 'ort' strategy.
 plugin/hooks/protect-paths.sh | 39 ++++++++++-----------------------------
 1 file changed, 10 insertions(+), 29 deletions(-)
```

### 5. Terminal Log: `git log --graph --oneline --decorate --all`

```text
*   b5d568f (HEAD -> main) merge: merge bugfix/hook-path into main
|\  
| * cef1bf7 (bugfix/hook-path) fix: expand HOME variable in hook protected paths
* |   b9ac550 merge: resolve merge conflict between feature/mcp-server and feature/skill-tests (selected v1.1.0)
|\ \  
| * | 6760015 (feature/skill-tests) feat: bump plugin version to 1.1.0 for skill-tests release
| * | ce50719 feat: add integration tests for EC2024A and lab sessions
| |/  
* |   ca48103 merge: feature/mcp-server into main
|\ \  
| |/  
|/|   
| * 17f0832 (feature/mcp-server) fix: bump plugin version to 1.0.1 — patch for MCP README addition
| * 4e22d5a docs: add MCP server README with JSON-RPC traces and security notes
|/  
* 7e58639 feat: initial commit — Nimbus Labs Campus Helpdesk Agent
```

---

### 6. Technical Worktree Architecture Analysis

#### Why Git Prevents Checking Out the Same Branch in Multiple Worktrees
When you run `git checkout feature/skill-tests` while another worktree already has it active, Git aborts with:
```text
fatal: 'feature/skill-tests' is already used by worktree at '/Users/ayushyadgiri/.gemini/antigravity/scratch/worktrees/feature-skill-tests'
```
This fundamental safeguard prevents **index and ref race conditions**. A Git branch ref is a single pointer (`refs/heads/<branch>`) stored in `.git`. If two working directories shared that branch, both could stage differing changes, update files independently, and attempt to write new commits advancing the same ref. This would cause catastrophic loss of uncommitted work and index corruption.

#### What is Shared vs. What is Separate
* **Shared Across All Worktrees:**
  - Common object database (`.git/objects/`): all commit objects, trees, and blobs are shared.
  - Refs namespace (`.git/refs/`): branch pointers, tags, and remotes.
  - Repository configuration (`.git/config`): shared unless `--worktree` scoped config is enabled.
  - Reflogs (`.git/logs/`): commit and ref histories.
* **Isolated Per Worktree:**
  - Working tree filesystem directory (all project files on disk).
  - Staging index (`.git/worktrees/<name>/index`).
  - Active branch pointer (`.git/worktrees/<name>/HEAD`).
  - Merge and cherry-pick state (`.git/worktrees/<name>/MERGE_HEAD`, etc.).

#### Safe Cleanup of Stale Worktrees
To safely clean worktrees without corrupting repository administrative metadata:
1. Ensure all changes are committed or stashed inside the worktree.
2. Remove using the official command: `git worktree remove <worktree-path>`.
3. If a worktree directory was manually deleted on disk, prune its administrative metadata using: `git worktree prune`.
4. Delete the associated feature branch once merged: `git branch -d <branch-name>`.

#### Claude Code `/worktree-merge` Audit
* **Status:** **UNVERIFIED / NON-EXISTENT**
* **Findings:** Official Anthropic Claude Code documentation does not define or recognize any built-in `/worktree-merge` slash command.
* **Why AI Merges Need Mandatory Human Review:** AI-assisted conflict resolution often prioritizes syntactic coherence over semantic correctness. For instance, in our `plugin.json` conflict, an automated agent might choose whichever branch it parsed last or naively concatenate version strings. In production codebases, automated AI merges can silently drop security patches, introduce logical regressions, or corrupt sensitive configurations without raising syntactic build errors. Human oversight remains essential.
