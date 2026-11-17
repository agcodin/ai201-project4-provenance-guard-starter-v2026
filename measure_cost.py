#!/usr/bin/env python3
"""
What one run costs. ← CAPSTONE, MILESTONE 3

Nothing here calls a hosted service, so the cost of a run is not money, it is
seconds of CPU on the machine it runs on. This times ten real submissions
through the live service and reports the average along with the spread, and it
times a guarded refusal separately, because the point of the guard is that a
refusal should cost almost nothing.

    python app.py                 # in one terminal
    python measure_cost.py        # in another
"""

import json
import statistics
import sys
import time

import requests

import calibrate
import config

BASE = f"http://{config.HOST}:{config.PORT}"
RUNS = 10


def time_post(body):
    started = time.perf_counter()
    response = requests.post(f"{BASE}/submit", json=body)
    wall = (time.perf_counter() - started) * 1000
    return wall, response


def main():
    texts = [t for _, t in calibrate.INPUTS]

    # One warm submission first. The model loads on the first call of the
    # process, and a 10-second load averaged into ten runs would report the
    # cost of starting the service rather than the cost of using it.
    time_post({"text": texts[0], "creator_id": "cost_warmup"})

    scored = []
    for i in range(RUNS):
        wall, response = time_post({
            "text": texts[i % len(texts)],
            "creator_id": f"cost_scored_{i}",
        })
        scored.append((wall, response.json().get("latency_ms")))

    refused = []
    for i in range(RUNS):
        wall, _ = time_post({"text": "word " * 800,
                             "creator_id": f"cost_refused_{i}"})
        refused.append(wall)

    walls = [w for w, _ in scored]
    served = [s for _, s in scored if s is not None]

    result = {
        "runs": RUNS,
        "scored_wall_ms_mean": round(statistics.mean(walls), 1),
        "scored_wall_ms_min": round(min(walls), 1),
        "scored_wall_ms_max": round(max(walls), 1),
        "scored_wall_ms_stdev": round(statistics.stdev(walls), 1),
        "scored_server_ms_mean": round(statistics.mean(served), 1) if served else None,
        "refused_wall_ms_mean": round(statistics.mean(refused), 1),
        "refused_wall_ms_max": round(max(refused), 1),
    }
    print(json.dumps(result, indent=2))

    config.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out = config.RESULTS_DIR / "cost.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    try:
        requests.post(f"{BASE}/ping", json={"message": "alive"}, timeout=5)
    except requests.RequestException:
        print(f"Nothing answering on {BASE}. Start the service first.",
              file=sys.stderr)
        sys.exit(1)
    main()
