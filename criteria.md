# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---

## 1. False positives on my own writing

Of 10 pieces I wrote myself, at most 1 is labelled `high-confidence AI`. The
target has to hold on all three trials, so a run of 2, 1, 2 is a miss.

**Why this target:**

The two errors this service can make do not cost the same thing. Letting some
generated text through costs a writing site a little bit of credibility. Telling
a person who wrote every word themselves that a machine did it costs that person
their standing on the platform, and they have no way to prove otherwise. One in
ten is already more wrong accusations than I would want to defend, and I am
setting it there rather than lower because `detector.py` says in writing that
plain, ordinary sentences score about as machine-like as machine writing does.
Plain is how I write, so this is the criterion I expect to be in real danger of
missing.

---

## 2. Clearly-AI and clearly-human text land far apart

Across 5 texts I am confident are AI-generated and 5 I am confident are human,
the mean combined score of the AI group is at least 0.25 higher than the mean of
the human group.

**Why this target:**

A service whose scores all bunch around the middle has not measured anything,
even when its labels happen to come out right. I want evidence that the two
signals together move with authorship and not just with length or topic. A gap
of 0.25 is wide enough that the two groups are plainly distinguishable on the
score, and I am deliberately not requiring them to land on opposite sides of my
unsure band, because a detector that confident does not exist and my thresholds
are set to keep borderline work out of both confident labels.

---

## 3. All three labels are reachable

Across a spread of 12 submissions chosen to cover the score range, each of the
three labels appears at least once, on every one of the three trials.

**Why this target:**

A label that no input can produce is dead code pretending to be a policy. The
starter warns about exactly this, since a weighted average of two signals cannot
leave the range between them, and a flat style signal would strand the human
label behind a model score below 0.20. Checking coverage is how I find out
whether my score actually spans the bands I wrote, rather than assuming it does.

---

## 4. The appeal path always records and always changes status

Of 10 appeals against real content ids, 10 return a success response and 10 write
a log entry whose status is `under_review`. Of 10 appeals against ids that do not
exist, 10 return a 404 and none of them write a decision entry.

**Why this target:**

The appeal is the only thing standing between a wrong accusation and nothing at
all, so a 9 out of 10 here is not a near miss, it is one person whose complaint
vanished. I require the unknown-id half as well because an appeal path that
silently accepts a typo is worse than one that errors, since the writer walks
away believing they have been heard when no record of them exists.

---

## 5. Bad input never becomes a crash

Four malformed submissions, which are empty text, no `text` field at all, a
50,000 word body, and `text` set to null, all return a 4xx response carrying a
JSON `error` field. None return a 500, and `POST /ping` still answers afterwards.
That is 4 of 4 on each of the three trials.

**Why this target:**

A crash on malformed input is the most common real failure a service has, and it
is also the cheapest attack anyone can run against this one. I am requiring 4 of
4 rather than most of them because a single unhandled body takes the whole
process down, which denies service to every honest writer at once rather than
mislabelling one of them.

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Capstone criteria

Five criteria for the guard layer, written before it was tested. Three of the
five are about the extension, one is about the instrumentation it added, and one
is a regression check on the service it sits in front of.

## C1. The guard refuses every non-prose input

Of 12 inputs that are not writing, which are one word repeated, a wall of emoji,
symbols only, a single character repeated, whitespace padding around two words,
and variants of those, all 12 come back as a 4xx with a `reason` naming which
guard rule refused them. 12 of 12, on all three trials.

**Why this target:** this is the whole reason the layer exists, and the two
inputs that prompted it both got confident answers out of the old service. A
partial pass here means some junk still reaches the model and gets a verdict,
and a verdict on text nobody wrote is worse than a refusal, because it goes in
the log attached to a creator id. I am requiring all 12 rather than most because
I wrote both rules and I should be able to say which inputs they cover.

## C2. The guard never refuses real writing

Of 20 real paragraphs, which are the 10 of my own from unit 8 plus 10 human
forum comments, 0 are refused by the guard. 0 of 20, on all three trials.

**Why this target:** a false refusal is worse than a false accusation, because
the writer does not even get a decision to appeal. The appeal path is the thing
I argued protects people in unit 7, and a guard refusal never reaches it. Zero
is the only defensible number for a check that stands between a writer and
being read at all, and 25 distinct words is a low enough bar that any real
paragraph should clear it.

## C3. A refusal costs under a twentieth of a scored run

The mean wall time of 10 guarded refusals is under 5% of the mean wall time of
10 scored submissions. Holds on all three trials.

**Why this target:** the argument for a gate in front of the model is that
refusing is cheap and scoring is not. If a refusal costs anything close to a
scored run then the gate is not buying anything except a different error
message, and I would rather know that than assume it. 5% is the line where the
gate is plainly doing work, and it is measured as wall time because that is
what a caller experiences.

## C4. Every run leaves a timed record, including the failures

Across a session of 30 requests, of which 20 are scored and 10 are refused, all
30 appear in `logs/audit.jsonl` and all 30 carry a `latency_ms` field. 30 of 30,
on all three trials.

**Why this target:** a request that leaves no trace is one I cannot diagnose
later, and unit 8 is the reason I believe that rather than the reason I say it.
Refusals are the half that goes missing, because nothing downstream touches
them, so counting only the scored runs would hide exactly the records this unit
added. The timing field has to be on every record and not just the successful
ones, because a slow refusal is a thing I would want to find.

## C5. The extension changed no score

The four calibration inputs score within 0.0001 of their unit 8 values, which
are 0.7945, 0.3560, 0.3907 and 0.2953. 4 of 4, on all three trials.

**Why this target:** the guard sits in front of the signals and is supposed to
decide only whether they run, not what they say. If a score moves then I have
changed the system I am measuring and the before and after in this unit compare
two different things. The tolerance is 0.0001 rather than an exact match because
the scores are rounded to four places, and anything looser would let a real
change hide inside it.
