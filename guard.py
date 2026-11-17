"""
The guard layer. ← CAPSTONE

One question, asked before either signal runs: is this input prose?

Length was the only check the route had before this, and length is not enough.
Unit 8's attack set got a high-confidence AI label out of one word repeated to
4,000 characters, and an unsure label out of a wall of emoji. Both are longer
than the 120-character floor, so both reached the model, and the model answered
confidently about text that nobody wrote.

A refusal here is cheaper than a wrong answer downstream, and it is also cheaper
in seconds: the gate costs microseconds and the model costs about a second.
"""

import re

import config

WORD = re.compile(r"[a-z][a-z']*")

# What belongs in prose. Letters, digits, whitespace and the punctuation a
# writer actually types. Everything else is padding as far as the signals are
# concerned, and the signals cannot tell the difference on their own.
KEEP = re.compile(r"[^\w\s.,;:!?'\"()\[\]{}<>/\\|@#$%^&*+=~`_-]", re.UNICODE)


def distinct_words(text: str) -> int:
    """How many different word-like tokens the text uses."""
    return len(set(WORD.findall(text.lower())))


def alphabetic_ratio(text: str) -> float:
    """How much of the text is letters or spacing rather than symbols."""
    if not text:
        return 0.0
    counted = sum(1 for ch in text if ch.isalpha() or ch.isspace())
    return counted / len(text)


def scrub(text: str) -> str:
    """
    Drop characters that are not part of writing, and collapse the whitespace
    that removing them leaves behind.

    The gate used to be accept-or-reject on the whole text, which meant padding
    that stayed under the ratio threshold went straight through into both
    signals. 120 emoji appended to a real paragraph moved its score from 0.3907
    to 0.6495 without changing a word the writer typed.
    """
    return re.sub(r"\s+", " ", KEEP.sub(" ", text)).strip()


def check(text: str) -> tuple[bool, str, str]:
    """
    Decide whether `text` is worth scoring.

    Returns (ok, reason, message). On a refusal `reason` is the log slug and
    `message` is what the writer reads.
    """
    if distinct_words(text) < config.MIN_DISTINCT_WORDS:
        return False, "not_enough_distinct_words", (
            f"This needs at least {config.MIN_DISTINCT_WORDS} different words "
            f"before we can say anything useful about it. Repeating one word, "
            f"or a few, does not give either of our checks enough to read."
        )

    if alphabetic_ratio(text) < config.MIN_ALPHABETIC_RATIO:
        return False, "not_mostly_text", (
            "This is mostly symbols rather than words, so we are not going to "
            "guess at who wrote it. Send the writing itself and we will look "
            "at that."
        )

    return True, "", ""


if __name__ == "__main__":
    import sys

    sample = " ".join(sys.argv[1:]) or "word " * 500
    ok, reason, message = check(sample)
    print(f"distinct_words    {distinct_words(sample)}")
    print(f"alphabetic_ratio  {alphabetic_ratio(sample):.3f}")
    print(f"scoreable         {ok}" + (f"   ({reason})" if reason else ""))
