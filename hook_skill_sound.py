#!/usr/bin/env python
"""PreToolUse hook: play a themed sound when a Claude Code skill fires.

Wire with matcher "Skill" so it only runs on the Skill tool. The hook reads the
PreToolUse JSON from stdin, maps tool_input.skill to a configured sound, and
plays it synchronously through play_sound.py so the interactive audio session
remains available.

Synchronous playback means the hook waits for the short clip (or timeout).
Playback failures are swallowed and the hook exits successfully instead of
failing the underlying tool call.

Matching: exact override first (SKILL_SOUNDS), then ordered substring patterns
(SKILL_PATTERNS). First match wins, so list the most specific keyword first
(e.g. "deep-audit" before a generic "audit"). Plugin-prefixed skill names such
as "ecc:code-review" are matched the same way.

This mapping reflects one OSINT/security workflow; edit it freely for your own
skills and sound stems.
"""
import sys
import os
import json
import subprocess

# Exact skill name -> sound stem (checked first; use for overrides)
SKILL_SOUNDS = {}

# Ordered (keyword, sound). First substring hit wins — specific before generic.
SKILL_PATTERNS = [
    ("deep-audit", "osint"),        # OSINT / forensic investigation
    ("osint", "osint"),
    ("genealog", "osint"),
    ("learn", "learn"),             # ecc:learn etc. -> "transfer of data complete"
    ("emergency", "redalert"),      # emergency-dump = panic
    ("security", "agentshield"),    # security-scan / security-review
    ("agentshield", "agentshield"),
    ("harness-audit", "agentshield"),
    ("review", "review"),           # code-review / *-review / review-pr
    ("checkpoint", "saved"),        # checkpoint / save -> "transfer complete"
    ("save-session", "saved"),
]

HERE = os.path.dirname(os.path.abspath(__file__))
PLAYER = os.path.join(HERE, "play_sound.py")


def pick_sound(skill):
    if skill in SKILL_SOUNDS:
        return SKILL_SOUNDS[skill]
    for keyword, sound in SKILL_PATTERNS:
        if keyword in skill:
            return sound
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    if data.get("tool_name") != "Skill":
        return
    skill = ((data.get("tool_input") or {}).get("skill", "") or "").strip().lower()
    sound = pick_sound(skill)
    if not sound:
        return
    try:
        subprocess.run([sys.executable, PLAYER, sound], timeout=10)
    except Exception:
        pass


if __name__ == "__main__":
    main()
    sys.exit(0)  # playback failure is non-fatal for the tool hook
