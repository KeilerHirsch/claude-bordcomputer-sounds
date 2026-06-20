# 🖖 claude-bordcomputer-sounds

Turn [Claude Code](https://docs.anthropic.com/en/docs/claude-code) into a Star-Trek-style ship's computer. Acoustic hook signals so you **hear** what Claude is doing without staring at the terminal — built for people who run Claude in auto-accept mode and tab away.

- ✅ **Done** signal when Claude finishes a turn (*"incoming transmission"*)
- 🔔 **Attention** chirp when Claude needs your input/permission
- 🚀 **Boot** voice on session start (*"command codes verified"*)
- 🧠 Themed sound when a specific skill fires (e.g. a research/audit skill)
- 🚨 **Red Alert** for dangerous commands, 🛑 voice for blocked actions (optional, wire into your own guard hooks)

No dependencies. Pure Python + native OS audio. Windows / macOS / Linux.

---

## Why

In auto-accept mode you don't watch every step — but you still want to know **the moment Claude is done** or **needs you**. A short, distinct sound does that better than glancing at the screen every 30 seconds. Tuned so it helps for hours instead of annoying you (see *Design* below).

---

## Install (2 minutes)

```bash
git clone https://github.com/KeilerHirsch/claude-bordcomputer-sounds.git
cd claude-bordcomputer-sounds
python download_sounds.py        # fetches the sounds (see Sounds & licensing)
python play_sound.py stop        # test: you should hear it
```

Then add the hooks to **`~/.claude/settings.json`** (merge with any existing `hooks`). Copy the blocks from [`settings.example.json`](settings.example.json) and replace `/ABS/PATH/TO` with your clone path. Minimal version:

```json
{
  "hooks": {
    "Stop":         [ { "hooks": [ { "type": "command", "command": "python /ABS/PATH/TO/claude-bordcomputer-sounds/play_sound.py stop",       "timeout": 8  } ] } ],
    "Notification": [ { "hooks": [ { "type": "command", "command": "python /ABS/PATH/TO/claude-bordcomputer-sounds/play_sound.py notify",     "timeout": 8  } ] } ],
    "PreCompact":   [ { "hooks": [ { "type": "command", "command": "python /ABS/PATH/TO/claude-bordcomputer-sounds/play_sound.py precompact", "timeout": 8  } ] } ],
    "SessionStart": [ { "hooks": [ { "type": "command", "command": "python /ABS/PATH/TO/claude-bordcomputer-sounds/play_sound.py boot",       "timeout": 10 } ] } ]
  }
}
```

**Restart your Claude Code session** (settings are read at launch). The next time Claude finishes a turn, you'll hear it. 🔊

---

## Event map

| Hook event | Fires when… | Sound (stem) | Frequency |
|---|---|---|---|
| `Stop` | Claude finishes a turn | `stop` — *incoming transmission* | very often |
| `Notification` | Claude needs permission / input | `notify` — combadge chirp | rare |
| `PreCompact` | context is about to be compacted | `precompact` — processing | rare |
| `SessionStart` | a session starts | `boot` — *command codes verified* | once/session |
| `PreToolUse` (`Skill`) | a mapped skill is invoked | `osint` — *accessing library computer data* | occasional |

Swap any clip by dropping your own `sounds/<stem>.mp3` in place.

---

## Design: cool, not annoying

The whole point is that it survives an 8-hour session. Two rules:

1. **Frequency × loudness.** Frequent events (`Stop`) use a short, calm clip. Rare events may be louder. Critical events (`redalert`) are meant to grab you — and almost never fire.
2. **Length caps.** Long ambient/klaxon clips are capped in `play_sound.py` (`CAPS`) so a 21-second alarm becomes a 4.5-second blast.

Deliberately **not** wired: a sound on every tool error or sub-agent stop — those fire too often and turn delight into noise.

### The one gotcha: don't mark the hooks `async`

If you add `"async": true`, Claude spawns the hook **detached**, which loses the interactive audio session — the sound "plays" but you hear nothing. Keep these hooks **synchronous**. The clips are short, so the tiny blocking cost is invisible.

---

## Optional: sound on a specific skill

[`hook_skill_sound.py`](hook_skill_sound.py) plays a sound when a chosen skill runs. Wire it as a `PreToolUse` hook with `matcher: "Skill"`, then edit the `SKILL_SOUNDS` map:

```python
SKILL_SOUNDS = {
    "my-research-skill": "osint",
    "my-deploy-skill":   "redalert",
}
```

It reads the tool payload on stdin, plays the mapped sound, and **never blocks** the tool.

---

## Optional: alerts from your own guard hooks

Have a hook that blocks secrets or dangerous commands? Call the player from it at the block point:

```python
import subprocess, sys, os
subprocess.run([sys.executable, os.path.join(HOOKS_DIR, "play_sound.py"), "redalert"])
```

`redalert` (klaxon) and `denied` (*"authorization required"*) ship for exactly this.

---

## Sounds & licensing

- **The code** in this repo is MIT (see [LICENSE](LICENSE)).
- **The sound clips are Star Trek sound effects © Paramount/CBS.** They are **not** included in this repo. `download_sounds.py` fetches them from [TrekCore](https://www.trekcore.com/audio/), which hosts them for **personal/fan use**. Use them privately; don't redistribute them.
- Prefer your own audio? Drop MP3s named `stop` / `boot` / `notify` / `precompact` / `redalert` / `denied` / `osint` into `sounds/` and skip the downloader. Everything is just file stems.

---

## Platform notes

- **Windows** — native MCI (`winmm.dll` via ctypes), plays MP3, supports caps.
- **macOS** — `afplay` (built in), caps via `-t`.
- **Linux** — first of `mpg123` / `ffplay` / `cvlc` / `paplay` found on `PATH`.

Sound fails silent everywhere: a missing player or clip never breaks your hook chain.

---

*Make it so.* 🚀
