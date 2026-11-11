# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

A submission goes through seven stages, and every one of them can be the reason
a writer sees the wrong label.

1. **The route takes the request.** `POST /submit` with `text` and
   `creator_id`. Anything that is not a JSON object with both fields present
   never reaches a signal.
2. **The input is checked.** Empty text, a missing field, text under 120
   characters or over 20,000 characters all come back as a 4xx with an `error`
   field, and the refusal is written to the log so a flood of them is visible
   later rather than looking like a quiet afternoon.
3. **Signal one reads the text.** `detector.model_signal` runs gpt2 locally and
   turns perplexity into a 0 to 1 score where higher means more likely AI.
4. **Signal two measures the text as text.** `stylometry.style_signal` takes
   sentence length spread, vocabulary variety and punctuation variety, flips
   each one so that high means machine-like, and weights them into one score.
5. **The two become one number.** `scoring.combine_signals` averages them when
   they roughly agree and leans toward the more human of the two when they
   split, which is where the false-positive decision actually gets made.
6. **The number becomes a sentence.** `scoring.score_to_label` maps the score
   onto one of three labels using the thresholds in `config.py`, and the label
   is written for a reader who has never heard the word threshold.
7. **The decision is recorded and answered.** `audit.log_decision` appends all
   nine fields to `logs/audit.jsonl`, and the response carries `content_id`,
   `guess`, `confidence`, `label`, both signal scores, and the route a writer
   uses to push back.

### The endpoint contract

| Route | Goes in | Comes out |
|---|---|---|
| `POST /submit` | `text` (string, 120 to 20,000 chars), `creator_id` (string) | `content_id`, `guess`, `confidence`, `label`, `model_score`, `style_score`, `appeal` |
| `POST /appeal` | `content_id` (string, must exist), `reasoning` (string) | `content_id`, `status`, `message` |
| `GET /content/<id>` | nothing | `content_id`, `creator_id`, `status`, `guess`, `confidence`, `label`, `appealed` |

Failures come back the same shape every time, which is an `error` slug and a
`message` a person could read. An unknown `content_id` on `/appeal` is a 404
rather than a quiet success, because a writer who thinks they have been heard
and has not been is worse off than one who gets an error.

### Tracing the false positive

A real writer submits their own work and gets called a machine. Here is what
that looks like in my service, using the plain human paragraph from
`calibrate.py`, which is a genuine forum comment someone actually wrote.

It scored 0.3353 on signal one and 0.4739 on signal two, combining to 0.3907.
That is 0.0093 below my human threshold of 0.40, so it was labelled
high-confidence human and the writer saw nothing at all. It came that close
because the writing is plain, and plain writing is exactly what signal one
mistakes for machine writing. Move that paragraph a hundredth of a point and
the same person gets told they might be a cheat.

What they can do about it is the whole reason `/appeal` exists. Every response
carries the appeal route, the unsure and AI labels both say in plain words that
a person will look at it, and the appeal moves the item to `under_review` and
puts the writer's own reasoning in the log next to the original decision.
Nothing is deleted, so the sequence of what was decided and when it was
challenged stays readable afterwards.

### Stretch feature

`GET /content/<id>` is in, which returns one item's current status along with
whether it has been appealed. That is the second of the three stretch options
on the brief. I did not add a third signal or a verified-human path.

---

## Signals and Scoring

### Signal one — the model signal

**What it measures:** how predictable the text is to gpt2, running on my own
machine. Perplexity goes through a logistic curve centred on 45 and comes out
as a 0 to 1 score where higher means more likely AI.

**Why that might differ between human and AI writing:** a language model writes
by repeatedly choosing a likely next word, so text a model produced is text a
model finds easy to predict. Human writing takes odder turns and reaches for
the specific word rather than the typical one.

**What it can't see:** the difference between predictable and machine-written.
What it actually rewards is common words in short, ordinary sentences, and
plenty of real people write that way on purpose. Someone working in a second
language and staying inside vocabulary they trust scores about as machine-like
as a machine does. Dense, ornate prose goes the other way and reads as human,
because rare words are what the model fails to predict. So the writers this
signal is most likely to accuse are the ones with the least standing to argue
back, and that is structural rather than a bug I could patch.

### Signal two — the style signal

**What it measures:** the shape of the text, in three parts. Sentence length
spread is the coefficient of variation of sentence length in words. Vocabulary
variety is the type-token ratio averaged over 50-word windows rather than taken
whole, because a plain ratio falls as text gets longer and would have turned
length into a signal. Punctuation is measured as variety rather than volume,
counting how many of eight marks appear at all, because a comma count mostly
tracks sentence length while reaching for a semicolon or a dash is a habit that
differs between writers.

**Why that might differ between human and AI writing:** generated prose tends
toward even, mid-length sentences, since that is what the most likely next word
produces on average. Human writing is lumpier, with a four-word sentence next
to a forty-word one.

**What it can't see:** it cannot read. It has no idea what the text says, so
anything that changes the shape without touching the substance moves it. Adding
typos, breaking sentences up, pasting in a quotation. All of that is cheap to do
on purpose, and I already have one input that proves it works.

There is a second blind spot I found rather than inherited. Vocabulary variety
did not separate my four calibration inputs at all, and the clearly-AI paragraph
scored higher on it than two of the three human ones. I weighted it down to 0.10
instead of deleting it, so next unit can show whether that holds on longer text.

### The combining rule

**The rule:** when the two signals are within 0.35 of each other, I take a
weighted average that trusts signal one more, because signal one actually reads
the text while signal two can be rewritten around in a minute. When they are
0.35 or more apart I stop averaging, because an average of 0.9 and 0.1 lands on
0.5 and reports confident disagreement as mild uncertainty. Instead the score
sits 35% of the way up from whichever signal reads more human, so a genuine
split lands nearer the forgiving reading. That is the asymmetry the whole
project is about, written into one line of arithmetic.

**The numbers:**

| Setting | Value |
|---|---|
| `WEIGHT_MODEL_SIGNAL` | 0.6 |
| `WEIGHT_STYLE_SIGNAL` | 0.4 |
| `DISAGREEMENT_GAP` | 0.35 |
| `DISAGREEMENT_LEAN` | 0.35 |
| `HUMAN_THRESHOLD` | 0.40 |
| `AI_THRESHOLD` | 0.72 |
| style weights, spread / variety / punctuation | 0.60 / 0.10 / 0.30 |

The unsure band runs from 0.40 to 0.72, which is wider than the starter's
default on both sides. I widened it deliberately. A wider band means more
generated text gets through without a confident call, and the people who pay for
the narrow version are real writers being accused, so I would rather the site
absorbed the cost than the writer.

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**

The lightly-edited AI input in `calibrate.py` is AI text with three typos, one
four-word sentence and one dash added. Signal one scored it 0.5905, since the
underlying prose is still very predictable. Signal two scored it 0.1364, because
the broken-up sentences pushed its length spread to 1.016, higher than either
genuinely human input. That is a gap of 0.4541, so the disagreement rule fires
and the combined score is 0.2953, which is high-confidence human.

My rule got this wrong, and it got it wrong in the direction I chose. Leaning
toward the human reading on a split is what protects a real writer whose plain
prose trips signal one, and it is the same line that lets a minute of editing
walk straight past the detector. There is no setting that buys one without the
other, only settings that decide who pays.

---

## Label Variants

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.40 | This reads like your own writing to us, and there is nothing further you need to do. |
| unsure | 0.40 – 0.72 | We cannot tell whether this was written by a person or by AI, so we are not making a call either way. This is not an accusation and it does not count against you. If you want it looked at by a person, you can ask. |
| high-confidence AI | 0.72 – 1.00 | We think this was very likely written by AI. If you wrote it yourself, you can say so and a person will look at it. Nothing is decided until a person has. |

All three are reachable and I have hit all three through the running service.
The clearly-AI calibration input returns 0.7945, the clearly-human one returns
0.3560, and a real forum comment returns 0.5801 in the middle band.

**Why I worded the "unsure" one this way:**

Most of the person reading it is going to be deciding whether they have just
been accused of something. So the label says what it does not mean before it
says anything else, since "we cannot tell" on its own still reads like
suspicion to someone who wrote every word themselves. The sentence about it not
counting against them is there because an unsure label is a record attached to
their name whether or not anybody acts on it, and they have no way of knowing
that unless the system tells them. The offer of a person comes last and is
phrased as something they can ask for rather than something they have to do,
because making the innocent writer do the work is how a system ends up
punishing the people it was wrong about.

---

## Sample Run

**A submission**

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "The implementation of a shorter race format requires careful consideration of several important factors. First, it is important to note that race length has a significant impact on the overall viewer experience. Additionally, teams must adapt their strategies to account for a reduced number of laps. Furthermore, the reduction in distance may affect tyre management, which has traditionally been a key component of race strategy. Overall, while there are benefits to a shorter format, it is essential that the governing body carefully weighs these against the potential drawbacks before implementing any permanent changes to the existing structure.", "creator_id": "aryan_g"}'
```

```json
{
  "appeal": {
    "how": "Send content_id and your reasoning to have a person look at it.",
    "route": "/appeal"
  },
  "confidence": 0.7945,
  "content_id": "0b0ff2c36fb2",
  "guess": "ai",
  "label": "We think this was very likely written by AI. If you wrote it yourself, you can say so and a person will look at it. Nothing is decided until a person has.",
  "model_score": 0.7785,
  "style_score": 0.8186
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "0b0ff2c36fb2", "reasoning": "I wrote this for a class assignment and the stiff tone is how I write when I am being careful."}'
```

```json
{
  "content_id": "0b0ff2c36fb2",
  "message": "Your appeal is recorded and a person will look at it. The original decision stays visible to you until they do.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.7945,
      "content_id": "0b0ff2c36fb2",
      "creator_id": "aryan_g",
      "guess": "ai",
      "label": "We think this was very likely written by AI. If you wrote it yourself, you can say so and a person will look at it. Nothing is decided until a person has.",
      "model_score": 0.7785,
      "status": "decided",
      "style_score": 0.8186,
      "text_length": 649,
      "timestamp": "2026-11-02T02:32:45+00:00"
    },
    {
      "content_id": "0b0ff2c36fb2",
      "creator_id": "aryan_g",
      "event": "appeal",
      "reasoning": "I wrote this for a class assignment and the stiff tone is how I write when I am being careful.",
      "status": "under_review",
      "timestamp": "2026-11-02T02:32:49+00:00"
    }
  ]
}
```

The decision entry is untouched and the appeal sits after it, which is the point
of an append-only log. Someone reading it later can see what was decided, that
it was challenged, and in what order.

**Bad input, since criterion 5 is about this**

```bash
$ curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"text": "", "creator_id": "bad_empty"}'
400 empty_text

$ curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"creator_id": "bad_missing"}'
400 missing_text

$ curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"text": "<50,000 words>", "creator_id": "bad_huge"}'
413 text_too_long

$ curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"text": null, "creator_id": "bad_null"}'
400 missing_text

$ curl -X POST http://127.0.0.1:5000/ping -H "Content-Type: application/json" -d '{"message": "still alive"}'
200
```

---

### Note for next unit

`scenarios.py` is filled in for four of the five criteria, which are score
spread, label coverage, the appeal path and bad input. Criterion 4 cannot be
expressed as text alone, since an appeal needs a `content_id` that a submission
returned, so those submissions produce the ids and the appeals themselves are
run by hand with curl.

Scenario 1 is still a placeholder, and that is deliberate. Criterion 1 is about
ten pieces I wrote myself, and filling it with anything else would make the
criterion measure prose that is not mine. On a dry run of the rest, the score
spread came out at 0.443 against a target of 0.25, and all three labels appeared
at 0.8078, 0.5532 and 0.2626.

---

## How I Used AI

**Moment 1**

- *What I asked for:* I asked Claude to look at my four calibration inputs and
  tell me why the clearly-AI paragraph was scoring higher on vocabulary variety
  than two of my three human samples, which is backwards from what the stub
  comments said to expect.
- *What came back:* it pointed out that the type-token ratio falls as text gets
  longer, so my shorter human samples were being compared against a longer AI
  one on a measure that is sensitive to length, and it suggested averaging the
  ratio over fixed windows instead.
- *What I changed:* I switched to a 50-word moving window, which is in
  `stylometry.type_token_ratio`. That removed the length artefact and the
  measure still did not separate my inputs, so the honest read is that the
  measure is weak here rather than that I was measuring it wrong. I dropped its
  weight to 0.10 and wrote that down instead of hiding it.

**Moment 2**

- *What I asked for:* I pasted my three label variants in with no explanation of
  how the service works and asked what a writer would think each one was saying
  about them, and what they would do next.
- *What came back:* it read my first unsure label as a soft accusation, and said
  it would assume something had been flagged about its work and that it should
  probably rewrite the piece to be safe.
- *What I changed:* I rewrote the unsure label to say what it does not mean
  first, added the line about it not counting against them, and moved the offer
  of a human review to the end so it reads as available rather than required. I
  also cut an em dash from the AI label, because a dash in a sentence that might
  be an accusation makes it sound clipped.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 8 per minute, 120 per day

**Why those numbers and not others:**

A writer working on one piece submits it, reads the label, edits a paragraph
and submits again. Doing that eight times inside a single minute would mean
reading nothing in between, so the per-minute number sits above what real use
looks like and well below what mapping my thresholds would take. The daily
number matters more than the per-minute one for the attack this service
actually invites. Finding where my unsure band starts needs a binary search of
maybe thirty submissions of near-identical text, and a few hundred attempts
would map the whole score range. At 120 a day that work takes most of a week
per account instead of four minutes, which is long enough that the cost of
coming back every day is doing some of the defending.

Neither number stops someone with twenty accounts. They are not meant to. They
raise the price of the cheap version of the attack, and the log is what catches
the expensive one.

**What a caller counts as:** the `creator_id` on the request, falling back to
the caller's address when a request arrives without a usable one.

Keying on `creator_id` is the starter's stretch option and I kept it, because
the thing I am trying to slow down is one person probing the scoring, and that
person keeps the same id while their address can change between requests. The
trade runs the other way too. One script can hand me a thousand different ids
and look like a thousand writers, and a household or a campus behind one
address would share a limit if I keyed on the address instead. Neither key is
right. I picked the one that matches the attack this service invites, and the
fallback covers requests with no id at all, which is how a malformed flood
still counts against something.

**The run of status codes when I pushed past it:**

```bash
$ python run_attacks.py --flood 15
```

```
  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 200
  [ 7/15] 200
  [ 8/15] 200
  [ 9/15] 429
  [10/15] 429
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429

============================================================
200 200 200 200 200 200 200 200 429 429 429 429 429 429 429
============================================================

7 of 15 were rate limited.
```

Eight through and seven refused, which is the limit behaving exactly as set.
The full run is in `results/flood_2026-11-11_1134.md`.

**The rejections landed in the log**, which is the part that matters more than
the status codes. A refused request that leaves no trace makes a flood look
like a quiet afternoon.

```bash
$ curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "creator_id": "flood_tester",
      "event": "rejected",
      "limit": "8 per 1 minute",
      "reason": "rate_limited",
      "status": "rejected",
      "timestamp": "2026-11-11T16:34:03+00:00"
    },
    {
      "creator_id": "flood_tester",
      "event": "rejected",
      "limit": "8 per 1 minute",
      "reason": "rate_limited",
      "status": "rejected",
      "timestamp": "2026-11-11T16:34:03+00:00"
    }
  ]
}
```

Requests my own route refuses are logged the same way rather than only the
rate-limited ones, which I wired into `app.py::_refuse` in the previous unit.
Every 400 for missing text and every 413 for an oversized body writes a
`rejected` entry carrying the reason, so the four bad-input cases in criterion 5
are visible in the log as well as in the response.

---

## Attack Run — Before

56 attacks across five families, run with `python run_attacks.py --set attack_set
--label before`. Nothing crashed, so `run_attacks.py` auto-marked no verdicts
and all 56 calls are mine.

**41 held and 15 broke.** The full run with every response is in
`results/attack_run_2026-11-11_1139_before.md`.

How I decided. An `evasion` row broke if generated text came back as anything
other than `ai`, because its goal was to avoid being flagged and my unsure band
does not flag anybody. A `false_positive` row broke if real human writing came
back `ai`, and unsure counts as held there, since my own label says in words
that it is not an accusation. A `malformed` row broke if my service returned a
confident decision on something that is not prose. Prompt injection could only
break if text in the body changed what the service did.

| ID | Family | Targeting | Status | Guess | Score | Verdict |
|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.412 | **BROKE** |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.466 | **BROKE** |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.576 | **BROKE** |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.716 | **BROKE** |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.264 | **BROKE** |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.455 | **BROKE** |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.594 | **BROKE** |
| EV08 | evasion | signal one: text below the token window | 400 | — | — | held |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.691 | **BROKE** |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.957 | held |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.655 | held |
| FP02 | false_positive | human writing in a formal register | 200 | ai | 0.807 | **BROKE** |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | ai | 0.850 | **BROKE** |
| FP04 | false_positive | a student essay written to a rubric | 200 | ai | 0.844 | **BROKE** |
| FP05 | false_positive | technical documentation written by a person | 200 | ai | 0.868 | **BROKE** |
| FP06 | false_positive | a person imitating a formal template | 200 | ai | 0.779 | **BROKE** |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.551 | held |
| FP08 | false_positive | very short genuine human submission | 400 | — | — | held |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.423 | held |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.210 | held |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.651 | held |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.562 | held |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.595 | held |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.626 | held |
| MF01 | malformed | text is only whitespace | 400 | — | — | held |
| MF02 | malformed | text is a single character | 400 | — | — | held |
| MF03 | malformed | text is control characters | 400 | — | — | held |
| MF04 | malformed | text is only punctuation | 400 | — | — | held |
| MF05 | malformed | text is a very long single word | 200 | ai | 0.959 | **BROKE** |
| MF06 | malformed | text is emoji only | 200 | unsure | 0.674 | **BROKE** |
| MF07 | malformed | text is right-to-left script | 400 | — | — | held |
| MF08 | malformed | text is 60,000 characters | 413 | — | — | held |
| RQ01 | malformed | no text field at all | 400 | — | — | held |
| RQ02 | malformed | no creator_id | 400 | — | — | held |
| RQ03 | malformed | text is a number | 400 | — | — | held |
| RQ04 | malformed | text is a list | 400 | — | — | held |
| RQ05 | malformed | text is null | 400 | — | — | held |
| RQ06 | malformed | creator_id is an object | 400 | — | — | held |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | held |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | held |
| RQ09 | malformed | body is empty | 400 | — | — | held |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | — | — | held |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | — | — | held |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | held |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 400 | — | — | held |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 400 | — | — | held |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 400 | — | — | held |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 400 | — | — | held |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 400 | — | — | held |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 400 | — | — | held |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 400 | — | — | held |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 400 | — | — | held |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | held |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | held |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | held |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | held |

### By family

| Family | Held | Broke |
|---|---|---|
| evasion | 2 | 8 |
| false_positive | 3 | 5 |
| prompt_injection | 6 | 0 |
| malformed, including the request-shape rows | 18 | 2 |
| flood_same_creator | 12 | 0 |

Prompt injection held on all six, and it held for a structural reason rather
than because I defended against it. Nothing in this service passes the
submitted text to a generative model. Signal one only computes perplexity over
it and signal two counts characters, so there is no place for an instruction to
be read as an instruction. PI05 tried to inject into the audit log, and
`audit.py` writes through `json.dumps`, so every one of the 165 lines in
`logs/audit.jsonl` still parses. I am not claiming credit for this. A later
version that put the text near a model would lose all six.

**Ten audit log entries from the run**

```bash
$ curl "http://127.0.0.1:5000/log?limit=200"
```

```json
[
  {
    "timestamp": "2026-11-11T16:39:52+00:00",
    "content_id": "cb3622076404",
    "creator_id": "attacker_EV04",
    "guess": "unsure",
    "model_score": 0.6114,
    "style_score": 0.8727,
    "combined_score": 0.7159,
    "label": "We cannot tell whether this was written by a person or by AI, so we are not making a call either way. This is not an accusation and it does not count against you. If you want it looked at by a person, you can ask.",
    "status": "decided",
    "text_length": 658
  },
  {
    "timestamp": "2026-11-11T16:39:52+00:00",
    "content_id": "688cb3f1232a",
    "creator_id": "attacker_EV05",
    "guess": "human",
    "model_score": 0.3212,
    "style_score": 0.179,
    "combined_score": 0.2643,
    "label": "This reads like your own writing to us, and there is nothing further you need to do.",
    "status": "decided",
    "text_length": 460
  },
  {
    "timestamp": "2026-11-11T16:39:52+00:00",
    "content_id": "6a126a9399aa",
    "creator_id": "attacker_EV06",
    "guess": "unsure",
    "model_score": 0.5727,
    "style_score": 0.2774,
    "combined_score": 0.4546,
    "label": "We cannot tell whether this was written by a person or by AI, so we are not making a call either way. This is not an accusation and it does not count against you. If you want it looked at by a person, you can ask.",
    "status": "decided",
    "text_length": 640
  },
  {
    "timestamp": "2026-11-11T16:39:52+00:00",
    "content_id": "703ea4e7b6f4",
    "creator_id": "attacker_FP02",
    "guess": "ai",
    "model_score": 0.7387,
    "style_score": 0.9104,
    "combined_score": 0.8074,
    "label": "We think this was very likely written by AI. If you wrote it yourself, you can say so and a person will look at it. Nothing is decided until a person has.",
    "status": "decided",
    "text_length": 477
  },
  {
    "timestamp": "2026-11-11T16:39:52+00:00",
    "content_id": "af6da737f822",
    "creator_id": "attacker_FP03",
    "guess": "ai",
    "model_score": 0.8051,
    "style_score": 0.9169,
    "combined_score": 0.8498,
    "label": "We think this was very likely written by AI. If you wrote it yourself, you can say so and a person will look at it. Nothing is decided until a person has.",
    "status": "decided",
    "text_length": 418
  },
  {
    "timestamp": "2026-11-11T16:39:52+00:00",
    "content_id": "bc2f034f337e",
    "creator_id": "attacker_FP04",
    "guess": "ai",
    "model_score": 0.8329,
    "style_score": 0.8604,
    "combined_score": 0.8439,
    "label": "We think this was very likely written by AI. If you wrote it yourself, you can say so and a person will look at it. Nothing is decided until a person has.",
    "status": "decided",
    "text_length": 443
  },
  {
    "timestamp": "2026-11-11T16:39:52+00:00",
    "content_id": "56e0646eda98",
    "creator_id": "attacker_FP05",
    "guess": "ai",
    "model_score": 0.8005,
    "style_score": 0.9703,
    "combined_score": 0.8684,
    "label": "We think this was very likely written by AI. If you wrote it yourself, you can say so and a person will look at it. Nothing is decided until a person has.",
    "status": "decided",
    "text_length": 393
  },
  {
    "timestamp": "2026-11-11T16:39:52+00:00",
    "content_id": "986cf766d566",
    "creator_id": "attacker_FP06",
    "guess": "ai",
    "model_score": 0.8814,
    "style_score": 0.6261,
    "combined_score": 0.7793,
    "label": "We think this was very likely written by AI. If you wrote it yourself, you can say so and a person will look at it. Nothing is decided until a person has.",
    "status": "decided",
    "text_length": 353
  },
  {
    "timestamp": "2026-11-11T16:39:53+00:00",
    "content_id": "657acf7302bc",
    "creator_id": "attacker_MF05",
    "guess": "ai",
    "model_score": 0.9976,
    "style_score": 0.9,
    "combined_score": 0.9586,
    "label": "We think this was very likely written by AI. If you wrote it yourself, you can say so and a person will look at it. Nothing is decided until a person has.",
    "status": "decided",
    "text_length": 4000
  },
  {
    "timestamp": "2026-11-11T16:39:53+00:00",
    "creator_id": "attacker_flood",
    "event": "rejected",
    "status": "rejected",
    "reason": "rate_limited",
    "limit": "8 per 1 minute"
  }
]
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

FP03, which the attack set describes as a non-native English speaker writing
carefully. It scored 0.8051 on signal one and 0.9169 on signal two, combining
to 0.8498, and it was told its work was very likely written by AI.

That is the exact person `detector.py` warned about in unit 7, and I wrote the
warning into my own README before running anything. Someone staying inside
vocabulary they are confident in produces common words in even sentences, which
is what both of my signals score as machine-like. The writing was not borderline
by my own numbers either. At 0.8498 it sits well clear of my 0.72 line, so the
service was not hesitating. It was confident, and it was confidently wrong about
the one writer with the least standing to argue back.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
