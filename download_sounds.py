#!/usr/bin/env python
"""Download the Bordcomputer sounds into sounds/.

The clips are Star Trek sound effects (c) Paramount/CBS, hosted by TrekCore
(https://www.trekcore.com/audio/) for personal/fan use. They are deliberately
NOT shipped in this repo — this script fetches them for your local install.
Prefer your own sounds? Drop MP3s named stop/boot/notify/precompact/redalert/
denied/osint into sounds/ and skip this script.
"""
import os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SNDDIR = os.path.join(HERE, "sounds")
BASE = "https://www.trekcore.com/audio/"

# local stem -> path on trekcore
MANIFEST = {
    "stop":       "computer/voice/incomingtransmission_clean.mp3",
    "boot":       "computer/voice/commandcodesverified_ep.mp3",
    "notify":     "communicator/tng_chirp_clean.mp3",
    "precompact": "computer/processing.mp3",
    "redalert":   "redalertandklaxons/tng_red_alert1.mp3",
    "denied":     "computer/voice/authorisationrequired_ep.mp3",
    "osint":      "computer/voice/accessinglibrarycomputerdata_clean.mp3",
}
UA = "Mozilla/5.0 (compatible; claude-bordcomputer-sounds)"


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
