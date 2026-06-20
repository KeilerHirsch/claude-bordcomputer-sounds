#!/usr/bin/env python
"""Optional PreToolUse hook: play a sound when a specific Claude Code skill fires.

Wire it with matcher "Skill" so it only runs on the Skill tool. It reads the
PreToolUse JSON on stdin, maps tool_input.skill -> a sound, and plays it via
play_sound.py (SYNC, to keep the interactive audio session). It NEVER blocks
the tool call.

Edit SKILL_SOUNDS to map YOUR skills to sounds. The example maps a couple of
research-type skills to the "osint" clip.
"""
import sys, os, json, subprocess

SKILL_SOUNDS = {
    # "your-skill-name": "sound-stem",
    "deep-audit": "osint",
    "osint-recherche": "osint",
}

HERE = os.path.dirname(os.path.abspath(__file__))
PLAYER = os.path.join(HERE, "play_sound.py")


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    if data.get("tool_name") != "Skill":
        return
    skill = ((data.get("tool_input") or {}).get("skill", "") or "").strip().lower()
    sound = SKILL_SOUNDS.get(skill)
    if not sound:
        return
    try:
        subprocess.run([sys.executable, PLAYER, sound], timeout=10)
    except Exception:
        pass


if __name__ == "__main__":
    main()
    sys.exit(0)  # never block the tool
