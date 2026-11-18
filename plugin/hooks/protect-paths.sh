#!/usr/bin/env bash
# protect-paths.sh — PreToolUse hook for campus-helpdesk plugin
#
# Purpose: Block any Write, Edit, or MultiEdit tool calls that target
# protected file paths. Outputs a non-zero exit code to abort the tool call.
#
# Receives: JSON payload via stdin from Claude Code (tool call details)
# Returns: Exit 0 to allow, Exit 2 to block with custom message
#
# IMPORTANT: This is a demonstration hook. It uses simple string matching
# on the tool input JSON passed via stdin. In production, use a proper
# JSON parser and more robust matching.
#
# Limitations of this demo:
#   - Relies on stdin JSON containing a "path" or "file_path" key
#   - Does not handle all edge cases (e.g. relative path traversal)
#   - Should be complemented by OS-level file permissions for real protection

set -euo pipefail

# Read the full tool-call JSON from stdin
TOOL_INPUT=$(cat)

# Protected path prefixes — no writes allowed to these
PROTECTED_PATHS=(
    "/etc/"
    "/usr/"
    "/var/"
    "/System/"
    "/Library/"
    "$HOME/.ssh"
    "$HOME/.gnupg"
    "$HOME/.aws"
    "$HOME/.claude"
    "plugin/hooks/"
    "plugin/plugin.json"
)

# Extract the file path from the tool input JSON using grep/sed
# (avoids requiring jq or Python in the hook environment)
FILE_PATH=$(echo "$TOOL_INPUT" | grep -oE '"(path|file_path|target_file)"\s*:\s*"[^"]*"' | head -1 | sed 's/.*: "//' | sed 's/"$//' || true)

if [ -z "$FILE_PATH" ]; then
    # No path found in payload — allow the call (may be a non-file tool)
    exit 0
fi

# Check against each protected path
for PROTECTED in "${PROTECTED_PATHS[@]}"; do
    if [[ "$FILE_PATH" == "$PROTECTED"* ]]; then
        echo "BLOCKED: Write to protected path '$FILE_PATH' is not permitted." >&2
        echo "Protected prefixes include system dirs, SSH keys, and plugin config files." >&2
        exit 2
    fi
done

# Path is safe — allow the tool call
exit 0
