#!/usr/bin/env bash
# protect-paths.sh — PreToolUse hook (BUGFIX: corrected path matching)
# Branch: bugfix/hook-path
# Fix: Added $HOME expansion to paths that previously used literal ~
set -euo pipefail

TOOL_INPUT=$(cat)

# Expanded protected paths (bugfix: ~ was not being expanded properly)
PROTECTED_PATHS=(
    "/etc/"
    "/usr/"
    "/var/"
    "/System/"
    "/Library/"
    "${HOME}/.ssh"
    "${HOME}/.gnupg"
    "${HOME}/.aws"
    "${HOME}/.claude"
    "plugin/hooks/"
    "plugin/plugin.json"
    "${HOME}/.zshrc"
    "${HOME}/.bashrc"
)

FILE_PATH=$(echo "$TOOL_INPUT" | grep -oE '"(path|file_path|target_file)"\s*:\s*"[^"]*"' | head -1 | sed 's/.*: "//' | sed 's/"$//' || true)

if [ -z "$FILE_PATH" ]; then
    exit 0
fi

for PROTECTED in "${PROTECTED_PATHS[@]}"; do
    if [[ "$FILE_PATH" == "$PROTECTED"* ]]; then
        echo "BLOCKED: Write to protected path '$FILE_PATH' is not permitted." >&2
        exit 2
    fi
done

exit 0
