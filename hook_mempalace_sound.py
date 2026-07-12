#!/usr/bin/env python
"""PreToolUse hook: play the "memory" sound when a memory store actually writes.

Example for the MemPalace MCP memory server, but the pattern works for any MCP
tool you want to flag. Wire with a matcher for your memory tools; this plays
only on real WRITE tools (not reads/searches), SYNC, and NEVER blocks.

>>> EDIT SAVE_TOOLS for your own memory/MCP write tools. <<<
"""
import sys
import os
import json
import subprocess

# MCP tool names that represent an actual memory WRITE (not a read/search)
SAVE_TOOLS = {
    "mcp__mempalace__mempalace_add_drawer",
    "mcp__mempalace__mempalace_update_drawer",
    "mcp__mempalace__mempalace_sync",
    "mcp__mempalace__mempalace_kg_add",
}

HERE = os.path.dirname(os.path.abspath(__file__))
PLAYER = os.path.join(HERE, "play_sound.py")


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    if data.get("tool_name") in SAVE_TOOLS:
        try:
            subprocess.run([sys.executable, PLAYER, "memory"], timeout=8)
        except Exception:
            pass


if __name__ == "__main__":
    main()
    sys.exit(0)  # never block the tool
