"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures ───────────────────────────────────────────────────────
# All three return "more human" as the HIGH end. style_signal flips them.

PUNCTUATION_KINDS = (",", ";", ":", "—", "–", "(", "?", "!")

MATTR_WINDOW = 50


def sentence_length_spread(text: str) -> float:
    """
    Coefficient of variation of sentence length in words. Higher means lumpier,
    which reads more human. A single sentence has no spread, so it returns 0.0
    and lands at the AI end by default.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n]
    if len(lengths) < 2:
        return 0.0

    mean = statistics.mean(lengths)
    if mean == 0:
        return 0.0
    return statistics.stdev(lengths) / mean


def type_token_ratio(text: str) -> float:
    """
    Vocabulary variety, between 0 and 1, higher meaning more varied.

    Averaged over 50-word windows rather than taken over the whole text,
    because a plain ratio falls as text gets longer and would turn length into
    a signal. Texts under one window fall back to the plain ratio.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    if len(tokens) <= MATTR_WINDOW:
        return len(set(tokens)) / len(tokens)

    windows = [
        len(set(tokens[i:i + MATTR_WINDOW])) / MATTR_WINDOW
        for i in range(len(tokens) - MATTR_WINDOW + 1)
    ]
    return statistics.mean(windows)


def punctuation_density(text: str) -> float:
    """
    How many of the eight tracked punctuation kinds the text uses at all,
    divided by eight. Variety rather than volume, because a comma count mostly
    tracks sentence length, while reaching for a semicolon or a dash is a habit
    that differs between writers.
    """
    return sum(1 for mark in PUNCTUATION_KINDS if mark in text) / len(PUNCTUATION_KINDS)


# ── Combining them ───────────────────────────────────────────────────────────
# Each measure gets a floor and a ceiling, and anything between them scales
# straight across. The anchors come from the four calibration inputs in
# calibrate.py and are written up in the README.

SPREAD_AI, SPREAD_HUMAN = 0.35, 0.70
VARIETY_AI, VARIETY_HUMAN = 0.62, 0.86
PUNCTUATION_AI, PUNCTUATION_HUMAN = 0.10, 0.375

# Variety is weighted down to almost nothing because it did not separate the
# calibration inputs at all — the clearly-AI paragraph scored HIGHER on it than
# two of the three human ones. Removing it would have been tidier, and leaving
# it in at 0.10 keeps the measure visible so unit 8 can show whether that holds
# on longer text.
WEIGHT_SPREAD = 0.60
WEIGHT_VARIETY = 0.10
WEIGHT_PUNCTUATION = 0.30


def _to_ai_score(value: float, ai_anchor: float, human_anchor: float) -> float:
    """One measure, flipped and rescaled so 1.0 is the AI end."""
    span = human_anchor - ai_anchor
    fraction = (value - ai_anchor) / span
    return min(max(1.0 - fraction, 0.0), 1.0)


def style_signal(text: str) -> float:
    """The style signal as a 0-1 score. Higher means more likely AI."""
    if not words(text):
        return 0.5

    spread = _to_ai_score(sentence_length_spread(text), SPREAD_AI, SPREAD_HUMAN)
    variety = _to_ai_score(type_token_ratio(text), VARIETY_AI, VARIETY_HUMAN)
    punctuation = _to_ai_score(
        punctuation_density(text), PUNCTUATION_AI, PUNCTUATION_HUMAN
    )

    return round(
        WEIGHT_SPREAD * spread
        + WEIGHT_VARIETY * variety
        + WEIGHT_PUNCTUATION * punctuation,
        4,
    )


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
    print("\nAll zeros? These are stubs — Milestone 4 is where you build them.")
