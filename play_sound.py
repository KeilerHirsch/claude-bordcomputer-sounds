#!/usr/bin/env python
# The Man, The Mythos, The Legend : KeilerHirsch
# Copyright (c) 2026 KeilerHirsch. Licensed under the GNU GPL v3 or later.
"""Bordcomputer sound player for Claude Code hooks.

Plays sounds/<name>.mp3 when called as:  play_sound.py <name>
Print clip durations with:                play_sound.py --info

Cross-platform, no third-party deps:
  - Windows : MCI via winmm.dll (ctypes) — plays MP3 natively, supports caps
  - macOS   : afplay
  - Linux   : first available of mpg123 / ffplay / cvlc / paplay

Runs SYNC. The Claude Code hooks that call this are NOT marked "async":
async hooks are spawned detached and lose the interactive audio session,
so the sound plays "successfully" but you hear nothing. Sync = audible.

Fails silent — a missing player or sound never breaks the hook chain.
"""
import sys
import os
import re
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SNDDIR = os.path.join(HERE, "sounds")

# Max playback ms per sound (only long clips need capping; rest play in full).
CAPS = {
    "redalert": 4500,   # the klaxon loop is ~21s -> cap to a 4.5s blast
}


# ---------- Windows (MCI) ----------
def _win_mci(cmd):
    import ctypes
    buf = ctypes.create_unicode_buffer(256)
    err = ctypes.windll.winmm.mciSendStringW(cmd, buf, 256, None)
    return err, buf.value


def _win_length_ms(path):
    _win_mci("close q")
    _win_mci(f'open "{path}" type mpegvideo alias q')
    _win_mci("set q time format milliseconds")
    _, val = _win_mci("status q length")
    _win_mci("close q")
    try:
        return int(val)
    except Exception:
        return -1


def _win_play(path, cap_ms):
    _win_mci("close bc")
    _win_mci(f'open "{path}" type mpegvideo alias bc')
    if cap_ms:
        _win_mci("set bc time format milliseconds")
        _win_mci(f"play bc from 0 to {cap_ms} wait")
    else:
        _win_mci("play bc wait")
    _win_mci("close bc")


# ---------- macOS / Linux ----------
def _unix_play(path, cap_ms):
    if sys.platform == "darwin":
        # afplay -t <seconds> caps duration
        cmd = ["afplay", path]
        if cap_ms:
            cmd = ["afplay", "-t", str(cap_ms / 1000.0), path]
        subprocess.run(cmd, timeout=30)
        return
    # Linux: pick the first available player
    for player in ("mpg123", "ffplay", "cvlc", "paplay"):
        if shutil.which(player):
            if player == "mpg123":
                subprocess.run([player, "-q", path], timeout=30)
            elif player == "ffplay":
                subprocess.run([player, "-nodisp", "-autoexit", "-loglevel", "quiet", path], timeout=30)
            elif player == "cvlc":
                subprocess.run([player, "--play-and-exit", "--intf", "dummy", path], timeout=30)
            else:  # paplay needs WAV; best-effort
                subprocess.run([player, path], timeout=30)
            return


def play(name):
    # A hook could hand us an unexpected name; only ever play a known-shaped stem
    # from our own sounds/ dir — never let it traverse the path or point elsewhere.
    if not re.fullmatch(r"[A-Za-z0-9_-]+", name or ""):
        return
    path = os.path.join(SNDDIR, f"{name}.mp3")
    if not os.path.exists(path):
        return
    cap = CAPS.get(name)
    try:
        if sys.platform == "win32":
            _win_play(path, cap)
        else:
            _unix_play(path, cap)
    except Exception:
        pass


def info():
    if not os.path.isdir(SNDDIR):
        print("no sounds/ dir — run download_sounds.py first")
        return
    for f in sorted(os.listdir(SNDDIR)):
        if f.lower().endswith(".mp3"):
            if sys.platform == "win32":
                print(f"{f:24} {_win_length_ms(os.path.join(SNDDIR, f)):>7} ms")
            else:
                print(f)


def main():
    if len(sys.argv) < 2:
        return
    if sys.argv[1] == "--info":
        info()
        return
    play(sys.argv[1])


if __name__ == "__main__":
    main()
