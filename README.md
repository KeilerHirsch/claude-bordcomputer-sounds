<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <img alt="Claude Bordcomputer Sounds" src="docs/logo-light.svg" width="470">
  </picture>
</div>

Turn [Claude Code](https://docs.anthropic.com/en/docs/claude-code) into a Star-Trek-style ship's computer. Acoustic hook signals so you **hear** what Claude is doing without staring at the terminal — built for people who run Claude in auto-accept mode and tab away.

> [!IMPORTANT]
> Enjoying this? You can support development on **[Ko-fi](https://ko-fi.com/keilerhirsch)** ☕ — please mention *Bordcomputer Sounds*.

- ✅ short **done** blip when Claude finishes a turn
- 🔔 **attention** chirp when Claude needs your input/permission
- 🚀 deep **power-up** on session start
- 🧠 themed **voice** when a skill runs (review, security scan, learn, OSINT…)
- 📼 **"regeneration cycle complete"** when your memory store writes
- 🛑 **"authorization required"** on a blocked action · 🚨 **Red Alert** on a dangerous one

No dependencies. Pure Python + native OS audio. Windows / macOS / Linux.

> **Heads up — this is tuned to *my* setup** (an OSINT/security workflow with a persistent memory store). That's on purpose: it's a **real, working example** of how far you can take Claude Code hooks, not a lowest-common-denominator toy. Everything is plain file-stems and small editable Python — **fork it and make it yours**: swap sounds, remap skills, delete what you don't want. The mapping below is a starting point, not a prescription.

---

## Why

In auto-accept mode you don't watch every step — but you still want to know **the moment Claude is done** or **needs you**. A short, distinct sound does that better than glancing at the screen every 30 seconds. Tuned so it helps for hours instead of annoying you (see *Design*).

---

## Install (2 minutes)

```bash
git clone https://github.com/KeilerHirsch/claude-bordcomputer-sounds.git
cd claude-bordcomputer-sounds
python download_sounds.py        # fetches the sounds (see Sounds & licensing)
python play_sound.py stop        # test: you should hear it
```

Then copy the hook blocks you want from [`settings.example.json`](settings.example.json) into **`~/.claude/settings.json`** (merge with any existing `hooks`), replacing `/ABS/PATH/TO` with your clone path. **Restart your Claude Code session** — settings are read at launch. The next finished turn will blip. 🔊

---

## Event map

| Hook event | Fires when… | Sound (stem) | Frequency |
|---|---|---|---|
| `Stop` | Claude finishes a turn | `stop` — short blip | very often |
| `Notification` | Claude needs permission / input | `notify` — combadge chirp | rare |
| `PreCompact` | context is about to be compacted (memory saves) | `memory` — *regeneration cycle complete* | rare |
| `SessionStart` | a session starts | `boot` — power-up | once/session |
| `PreToolUse` (`Skill`) | a skill runs | mapped voice (see below) | occasional |
| `PreToolUse` (memory MCP write) | your memory store writes a record | `memory` | occasional |

### Skill voices (via `hook_skill_sound.py`, substring match)
| Skill keyword | Sound |
|---|---|
| `*-review` (code/pr/lang) | `review` — *diagnostic complete* |
| `security` / `scan` / `audit` | `agentshield` — *automatic defense procedures initiated* |
| `checkpoint` / `save` | `saved` — *transfer complete* |
| `learn` | `learn` — *transfer of data complete* |
| `deep-audit` / `osint` / `genealogy` | `osint` — *accessing library computer data* |
| `emergency` | `redalert` 🚨 |

---

## Design: cool, not annoying

The whole point is to survive an 8-hour session:

1. **Frequency × loudness.** The most frequent event (`Stop`) uses the shortest, calmest blip. Voice lines only fire on rarer events. Critical sounds (`redalert`) are meant to grab you — and almost never fire.
2. **Length caps.** Long ambient/klaxon clips are capped in `play_sound.py` (`CAPS`) so a 21-second alarm becomes a 4.5-second blast.
3. **Memory sound only on *real* saves.** The memory store writes on every turn under the hood — but the sound only fires on `PreCompact` and explicit record writes, never on every `Stop`. No double-blip.

Deliberately **not** wired: a sound on every tool error, sub-agent stop, or build/test step — those fire too often and turn delight into noise.

### The one gotcha: don't mark the hooks `async`

If you add `"async": true`, Claude spawns the hook **detached**, which loses the interactive audio session — the sound "plays" but you hear nothing. Keep these hooks **synchronous**. The clips are short, so the blocking cost is invisible.

---

## Customizing

- **Different sounds:** drop your own `sounds/<stem>.mp3` in place. Done.
- **Map your skills:** edit `SKILL_PATTERNS` in [`hook_skill_sound.py`](hook_skill_sound.py) — ordered `(keyword, sound)` pairs, most specific first.
- **Memory / any MCP tool:** edit `SAVE_TOOLS` in [`hook_mempalace_sound.py`](hook_mempalace_sound.py) to flag any MCP write tool you care about.
- **Alerts from your own guard hooks:** call the player from a hook at its block point — `redalert` (klaxon) and `denied` (*authorization required*) ship for exactly this:
  ```python
  import subprocess, sys, os
  subprocess.run([sys.executable, os.path.join(HOOKS_DIR, "play_sound.py"), "redalert"])
  ```

---

## Sounds & licensing

- **The code** in this repo is GPLv3 (see [LICENSE](LICENSE)).
- **The sound clips are Star Trek sound effects © Paramount/CBS.** They are **not** included here. `download_sounds.py` fetches them from [TrekCore](https://www.trekcore.com/audio/), which hosts them for **personal/fan use**. Use them privately; don't redistribute them.
- Prefer your own audio? Use any MP3s with the stem names from `download_sounds.py` and skip the downloader.

---

## Platform notes

- **Windows** — native MCI (`winmm.dll` via ctypes), plays MP3, supports caps.
- **macOS** — `afplay` (built in), caps via `-t`.
- **Linux** — first of `mpg123` / `ffplay` / `cvlc` / `paplay` found on `PATH`.

Sound fails silent everywhere: a missing player or clip never breaks your hook chain.

---

## Part of a bigger picture

This sound layer is the fun, surface-level piece of a much deeper setup. It hangs off a persistent memory store and a stack of guard hooks — because the interesting question isn't "can Claude make a noise," it's **"what actually makes an AI assistant reliable enough to trust on real work?"**

That's a separate, more serious project: **[ai-trinity](https://github.com/KeilerHirsch/ai-trinity)** — *a great model is not enough.* Three pillars that make Claude actually dependable: a model you've **proven** isn't bluffing, a solid **foundation/method**, and a **persistent brain** (memory). If the hooks here made you curious how the rest fits together, that's the map. 🖖

---

*Make it so.* 🚀
