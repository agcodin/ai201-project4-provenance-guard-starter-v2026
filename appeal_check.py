#!/usr/bin/env python3
"""
Criterion 4 across three trials. ← UNIT 8, MILESTONE 3

An appeal needs a content_id that a submission returned, so this cannot be
expressed as a scenario in scenarios.py. It submits ten pieces, appeals against
all ten ids, then appeals against ten ids that do not exist, and checks the log
moved each real one to under_review.

    python appeal_check.py            # three trials, writes results/appeals_<date>.md
"""

import datetime as dt
import json
import sys
import uuid
from pathlib import Path

import requests

import config
import scenarios

BASE = f"http://{config.HOST}:{config.PORT}"
TRIALS = 3


def texts():
    """Ten submissions, taken from the scenarios already written for criterion 2."""
    pool = scenarios.SCENARIOS[1]["texts"]
    return pool[:10]


def one_trial(trial):
    recorded = 0
    status_changed = 0
    unknown_rejected = 0
    unknown_logged = 0

    for i, text in enumerate(texts()):
        creator = f"appeal_t{trial}_{i}"
        sub = requests.post(f"{BASE}/submit",
                            json={"text": text, "creator_id": creator})
        if sub.status_code != 200:
            continue
        content_id = sub.json()["content_id"]

        app = requests.post(f"{BASE}/appeal", json={
            "content_id": content_id,
            "reasoning": "I wrote this myself and I would like a person to read it.",
        })
        if app.status_code == 200:
            recorded += 1
        if app.status_code == 200 and app.json().get("status") == "under_review":
            status_changed += 1

        status = requests.get(f"{BASE}/content/{content_id}").json().get("status")
        if status == "under_review":
            unknown_logged += 1

    for _ in range(10):
        missing = requests.post(f"{BASE}/appeal", json={
            "content_id": uuid.uuid4().hex[:12],
            "reasoning": "This id does not exist.",
        })
        if missing.status_code == 404:
            unknown_rejected += 1

    return {
        "trial": trial,
        "appeals_accepted": f"{recorded}/10",
        "status_under_review_in_response": f"{status_changed}/10",
        "status_under_review_in_log": f"{unknown_logged}/10",
        "unknown_ids_rejected_404": f"{unknown_rejected}/10",
    }


def main():
    try:
        requests.post(f"{BASE}/ping", json={"message": "alive"}, timeout=5)
    except requests.RequestException:
        print(f"Nothing answering on {BASE}. Start the service first.",
              file=sys.stderr)
        sys.exit(1)

    results = [one_trial(t) for t in range(1, TRIALS + 1)]
    for row in results:
        print(json.dumps(row))

    config.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    out = config.RESULTS_DIR / f"appeals_{stamp}.md"
    lines = ["# Criterion 4 — the appeal path", "",
             f"- {TRIALS} trials · {stamp}", "",
             "```json", json.dumps(results, indent=2), "```", ""]
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
