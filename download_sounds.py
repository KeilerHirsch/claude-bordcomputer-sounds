#!/usr/bin/env python
"""Download the Bordcomputer sounds into sounds/.

The clips are Star Trek sound effects (c) Paramount/CBS, hosted by TrekCore
(https://www.trekcore.com/audio/) for personal/fan use. They are deliberately
NOT shipped in this repo — this script fetches them for your local install.
Prefer your own sounds? Drop MP3s with the same stem names into sounds/ and
skip this script. Everything is just file stems.
"""
import os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SNDDIR = os.path.join(HERE, "sounds")
BASE = "https://www.trekcore.com/audio/"

# local stem -> path on trekcore. This is the author's curated TNG set; swap
# freely. Stems map to events/skills in settings.example.json + the hooks.
MANIFEST = {
    # native events
    "stop":        "computer/input_ok_1_clean.mp3",                 # short "done" blip
    "boot":        "other/power_up1_clean.mp3",                     # deep power-up on session start
    "notify":      "communicator/tng_chirp_clean.mp3",             # combadge chirp = needs you
    # skill sounds (see hook_skill_sound.py)
    "osint":       "computer/voice/accessinglibrarycomputerdata_clean.mp3",
    "learn":       "computer/voice/transferofdatacomplete.mp3",
    "agentshield": "computer/voice/automaticdefenseproceduresinitiated.mp3",
    "review":      "computer/voice/diagnosticcomplete_ep.mp3",
    "saved":       "computer/voice/transfercomplete_clean.mp3",
    # security / alerts (wire into your own guard hooks)
    "denied":      "computer/voice/authorisationrequired_ep.mp3",
    "redalert":    "redalertandklaxons/tng_red_alert1.mp3",
    # memory store (see hook_mempalace_sound.py + PreCompact)
    "memory":      "computer/voice/regeneration_cycle_complete.mp3",
}
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) claude-bordcomputer-sounds"


def fetch(stem, path):
    dest = os.path.join(SNDDIR, stem + ".mp3")
    req = urllib.request.Request(BASE + path, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
    except Exception as e:
        print(f"  ! {stem}: download failed ({e})")
        return False
    if data[:3] != b"ID3" and data[:2] != b"\xff\xfb":
        print(f"  ! {stem}: not an MP3 ({len(data)}B) — skipped")
        return False
    with open(dest, "wb") as f:
        f.write(data)
    print(f"  + {stem}.mp3 ({len(data)} bytes)")
    return True


def main():
    os.makedirs(SNDDIR, exist_ok=True)
    print("Downloading Bordcomputer sounds from TrekCore (fan-use)...")
    ok = sum(fetch(s, p) for s, p in MANIFEST.items())
    print(f"Done: {ok}/{len(MANIFEST)} sounds -> {SNDDIR}")
    if ok < len(MANIFEST):
        sys.exit(1)


if __name__ == "__main__":
    main()
