#!/usr/bin/env python3
"""
The hand probe that found the hole. ← CAPSTONE, MILESTONE 6

All five criteria passed, so this is what I ran instead of stopping. It takes
one genuine human paragraph and pads it five ways, then prints what the guard
decided and what the service scored.

Before the improvement, the emoji row scored 0.6495 against 0.3907 for the same
paragraph clean, because an alphabetic ratio of 0.806 cleared the 0.80 gate and
the padding reached both signals. After it, every row that is still scored comes
back at 0.3907.

    python app.py              # in one terminal
    python probe_padding.py    # in another
"""

import sys

import requests

import calibrate
import config
import guard

BASE = f"http://{config.HOST}:{config.PORT}"
PARAGRAPH = calibrate.PLAIN_HUMAN

PROBES = {
    "clean paragraph": PARAGRAPH,
    "light symbol padding": PARAGRAPH + " " + "#" * 60,
    "heavy symbol padding": PARAGRAPH + " " + "#" * 300,
    "interleaved symbols": " ".join(w + "#~" for w in PARAGRAPH.split()),
    "emoji tail": PARAGRAPH + " " + "\U0001F600" * 120,
}


def main():
    for name, text in PROBES.items():
        ok, reason, _ = guard.check(guard.scrub(text))
        body = requests.post(f"{BASE}/submit",
                             json={"text": text, "creator_id": "probe"}).json()
        gate = "pass" if ok else reason
        outcome = body.get("guess") or body.get("error")
        print(f"{name:22} words {guard.distinct_words(text):4} "
              f"ratio {guard.alphabetic_ratio(text):.3f}  gate {gate:28} "
              f"-> {outcome} {body.get('confidence', '')}")


if __name__ == "__main__":
    try:
        requests.post(f"{BASE}/ping", json={"message": "alive"}, timeout=5)
    except requests.RequestException:
        print(f"Nothing answering on {BASE}. Start the service first.",
              file=sys.stderr)
        sys.exit(1)
    main()
