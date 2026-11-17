#!/usr/bin/env python3
"""
The five capstone criteria, three trials each. ← CAPSTONE, MILESTONE 5

    python app.py                              # in one terminal
    python capstone_eval.py                    # in another
    python capstone_eval.py --label before

Writes results/capstone_<label>.json with every response, so the verdicts in the
README come from recorded output rather than from what I remember seeing.
"""

import argparse
import json
import statistics
import sys
import time

import requests

import audit
import calibrate
import config
import scenarios

BASE = f"http://{config.HOST}:{config.PORT}"

NOT_PROSE = [
    "word " * 800,
    "\U0001F600" * 200,
    "#$%^&*()" * 40,
    "a" * 900,
    "   ok   " * 60,
    "la la la la " * 80,
    "123 456 789 " * 70,
    "-" * 500,
    "\U0001F680\U0001F525" * 150,
    "test test test test " * 50,
    "• " * 300,
    "yes no yes no " * 60,
]

EXTRA_HUMAN = [
    'Indeed, the argument from Vowles sounds flawed. Their disadvantage (of not having proper basic systems in place) exists regardless of a cost cap. The cost cap likely forces them to divert resources from the car and towards those systems, and if they should have the resources for both, this restriction must be frustrating in the short term. But once they are up to speed, it is the very cost cap that will ensure level playing field and a realistic chance at success. The price is, optimistically, a few lean years before they are truly in the running.',
    'Back in 2010 newcomers Lotus, Virgin and Hispania were promised a cost cap system, and that was one of the reasons they risked entering the sport, otherwise they stood no chance of competing with the established giants. Without eventually introducing it, they ended up miles away even from the back of the midfield and left empty handed only a couple of seasons later, with (on their own level) enermous resources invested but gained nothing in return. Without the cost cap, I don’t think we’d be able to watch a 22 car grid these days.',
    'The current technical regs are way too tight. The cost cap has not achieved what it was supposed to. F1 would be better off with something like a MotoGP claiming rule, or it could introduce different kinds of limitation (perhaps 50Kg of fuel?) while at the same time relaxing the technical regs so that engineers can properly innovate again rather than tinker at the edges. Maybe even have dual tech streams and allow teams that follow one route more leeway in some area. They did that in the 80s, sort of. F1’s current trajectory is not good. The people who run it seem to have lost their way.',
    'No I think that’s flawed thinking. I’ve mentioned this before, but if you took away a lot of restrictions you’d have ways around the cost cap. You’d have supercar manufacturers and/or hypercar competitors using their road car divisions to find gains that they then “inherit” for free in F1. Then teams like Red Bull and Williams stand no chance. Restrictions should only be relaxed on things which are specific to F1. There’s a lower limit of 12kg on the weight of the turbochargers, for example. If this wasn’t in place, it’s an arms race which could be funded via research in road and other motorsports categories.',
    'Red Bull has already competed against powerhouse automakers like Toyota, BMW and Honda and beaten them. Indeed, and that’s my point. It was done in the days when there wasn’t a cost cap. Now with a cost cap, Red Bull wouldn’t be fighting a fair fight. Toyota and BMW participate in the hypercar class of WEC, and without restrictions on F1 parts, plenty of hypercar research could find its way into BMW and Toyota’s F1 cars (were BMW and Toyota still in F1) essentially for free.',
]

UNIT8_SCORES = [0.7945, 0.3560, 0.3907, 0.2953]


def post(text, creator):
    started = time.perf_counter()
    response = requests.post(f"{BASE}/submit",
                             json={"text": text, "creator_id": creator})
    return (time.perf_counter() - started) * 1000, response


def real_paragraphs():
    """
    The 20 real paragraphs criterion C2 names: my own 10 from unit 8, the 5
    human forum comments already in scenarios.py, and 5 more from the same
    source. The first version of this function returned 15, which quietly made
    C2 and C4 measure a smaller set than their own targets.
    """
    mine = scenarios.SCENARIOS[0]["texts"]
    humans = scenarios.SCENARIOS[1]["texts"][5:] + EXTRA_HUMAN
    return mine + humans


def c1(trial):
    rows = []
    for i, text in enumerate(NOT_PROSE):
        _, response = post(text, f"c1_t{trial}_{i}")
        body = response.json()
        rows.append({"status": response.status_code,
                     "reason": body.get("error")})
    passed = sum(1 for r in rows
                 if 400 <= r["status"] < 500 and r["reason"] in
                 ("not_enough_distinct_words", "not_mostly_text"))
    return f"{passed}/{len(NOT_PROSE)}", rows


def c2(trial):
    texts = real_paragraphs()
    refused = []
    for i, text in enumerate(texts):
        _, response = post(text, f"c2_t{trial}_{i}")
        if response.status_code != 200:
            refused.append({"index": i, "status": response.status_code,
                            "reason": response.json().get("error")})
    return f"{len(refused)}/{len(texts)}", refused


def c3(trial):
    scored = [post(t, f"c3_t{trial}_s{i}")[0]
              for i, t in enumerate([t for _, t in calibrate.INPUTS] * 3)][:10]
    refused = [post("word " * 800, f"c3_t{trial}_r{i}")[0] for i in range(10)]
    ratio = statistics.mean(refused) / statistics.mean(scored)
    return round(ratio, 5), {
        "scored_mean_ms": round(statistics.mean(scored), 1),
        "refused_mean_ms": round(statistics.mean(refused), 1),
        "ratio": round(ratio, 5),
    }


def c4(trial):
    before = len(audit.read_entries())
    creators = []
    for i, text in enumerate(real_paragraphs()):
        creator = f"c4_t{trial}_s{i}"
        post(text, creator)
        creators.append(creator)
    for i in range(10):
        creator = f"c4_t{trial}_r{i}"
        post("word " * 800, creator)
        creators.append(creator)

    entries = audit.read_entries()[before:]
    mine = [e for e in entries if e.get("creator_id") in set(creators)]
    timed = [e for e in mine if e.get("latency_ms") is not None]
    return f"{len(timed)}/30", {
        "entries_found": len(mine),
        "entries_with_latency": len(timed),
        "sample": mine[-2:],
    }


def c5(trial):
    rows = []
    for i, (name, text) in enumerate(calibrate.INPUTS):
        _, response = post(text, f"c5_t{trial}_{i}")
        rows.append({"input": name,
                     "confidence": response.json().get("confidence"),
                     "unit8": UNIT8_SCORES[i]})
    passed = sum(1 for r in rows
                 if r["confidence"] is not None
                 and abs(r["confidence"] - r["unit8"]) <= 0.0001)
    return f"{passed}/4", rows


CRITERIA = [("C1", c1), ("C2", c2), ("C3", c3), ("C4", c4), ("C5", c5)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", default="")
    args = parser.parse_args()

    out = {"label": args.label, "trials": {}}
    for trial in (1, 2, 3):
        out["trials"][trial] = {}
        for name, fn in CRITERIA:
            measure, detail = fn(trial)
            out["trials"][trial][name] = {"measure": measure, "detail": detail}
            print(f"trial {trial}  {name}  {measure}")
        print()

    config.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    suffix = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"capstone{suffix}.json"
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    try:
        requests.post(f"{BASE}/ping", json={"message": "alive"}, timeout=5)
    except requests.RequestException:
        print(f"Nothing answering on {BASE}. Start the service first.",
              file=sys.stderr)
        sys.exit(1)
    main()
