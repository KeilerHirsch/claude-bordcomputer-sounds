#!/usr/bin/env python
"""PreToolUse hook: play a themed sound when a Claude Code skill fires.

Wire with matcher "Skill" so it only runs on the Skill tool. Reads the
PreToolUse JSON on stdin, picks a sound for tool_input.skill, plays it via
play_sound.py (SYNC, to keep the interactive audio session). NEVER blocks.

Matching: exact override first (SKILL_SOUNDS), then ordered substring patterns
(SKILL_PATTERNS) — first hit wins, so list the MOST SPECIFIC keyword first
(e.g. "deep-audit" before the generic "audit"). Works for plain and
plugin-prefixed skill names alike (e.g. "ecc:code-review" matches "review").

>>> This is the author's mapping (OSINT/security workflow). EDIT freely:
    add your own (keyword, sound) pairs, point them at your own MP3 stems. <<<
"""
import sys, os, json, subprocess

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
    sys.exit(0)  # never block the tool
