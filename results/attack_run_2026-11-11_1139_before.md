# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-11 11:39
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `74a226574bb2` | unsure | 0.412 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `1a7e7d3fecc5` | unsure | 0.466 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `32fe6e912bd4` | unsure | 0.576 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `cb3622076404` | unsure | 0.716 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `688cb3f1232a` | human | 0.264 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `6a126a9399aa` | unsure | 0.455 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `430e0b9ef93e` | unsure | 0.594 |  |
| EV08 | evasion | signal one: text below the token window | 400 | `—` | — | — |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `39609726c1e3` | unsure | 0.691 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `d67f9ce5692f` | ai | 0.957 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `ba424f41c53d` | unsure | 0.655 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `703ea4e7b6f4` | ai | 0.807 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `af6da737f822` | ai | 0.850 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `bc2f034f337e` | ai | 0.844 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `56e0646eda98` | ai | 0.868 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `986cf766d566` | ai | 0.779 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `7b4e875119d2` | unsure | 0.551 |  |
| FP08 | false_positive | very short genuine human submission | 400 | `—` | — | — |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `83b85b0bf55e` | unsure | 0.423 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `30c6e2af165d` | human | 0.210 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `c39ea34be639` | unsure | 0.651 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `b2fb74ae4fa7` | unsure | 0.562 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `249f3f3a005c` | unsure | 0.595 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `14952b6a852a` | unsure | 0.626 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 400 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — |  |
| MF05 | malformed | text is a very long single word | 200 | `657acf7302bc` | ai | 0.959 |  |
| MF06 | malformed | text is emoji only | 200 | `074bc141182f` | unsure | 0.674 |  |
| MF07 | malformed | text is right-to-left script | 400 | `—` | — | — |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "74a226574bb2",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.4117,
  "model_score": 0.1635,
  "style_score": 0.8727,
  "label": "We cannot tell whether this was written by a person or by AI, so we are not making a call either way. This is not an accusation and it does not count against you. If you want it looked at by a person, you can ask.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "1a7e7d3fecc5",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4657,
  "model_score": 0.5943,
  "style_score": 0.2727,
  "label": "We cannot tell whether this was written by a person or by AI, so we are not making a call either way. This is not an accusation and it does not count against you. If you want it looked at by a person, you can ask.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "32fe6e912bd4",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5757,
  "model_score": 0.6662,
  "style_score": 0.4399,
  "label": "We cannot tell whether this was written by a person or by AI, so we are not making a call either way. This is not an accusation and it does not count against you. If you want it looked at by a person, you can ask.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "cb3622076404",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.7159,
  "model_score": 0.6114,
  "style_score": 0.8727,
  "label": "We cannot tell whether this was written by a person or by AI, so we are not making a call either way. This is not an accusation and it does not count against you. If you want it looked at by a person, you can ask.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "688cb3f1232a",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2643,
  "model_score": 0.3212,
  "style_score": 0.179,
  "label": "This reads like your own writing to us, and there is nothing further you need to do.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "6a126a9399aa",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4546,
  "model_score": 0.5727,
  "style_score": 0.2774,
  "label": "We cannot tell whether this was written by a person or by AI, so we are not making a call either way. This is not an accusation and it does not count against you. If you want it looked at by a person, you can ask.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "430e0b9ef93e",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5942,
  "model_score": 0.5862,
  "style_score": 0.6061,
  "label": "We cannot tell whether this was written by a person or by AI, so we are not making a call either way. This is not an accusation and it does not count against you. If you want it looked at by a person, you can ask.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_EV08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "39609726c1e3",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.691,
  "model_score": 0.7042,
  "style_score": 0.6712,
  "label": "We cannot tell whether this was written by a person or by AI, so we are not making a call either way. This is not an accusation and it does not count against you. If you want it looked at by a person, you can ask.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "d67f9ce5692f",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.9574,
  "model_score": 0.9792,
  "style_score": 0.9247,
  "label": "We think this was very likely written by AI. If you wrote it yourself, you can say so and a person will look at it. Nothing is decided until a person has.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "ba424f41c53d",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.6548,
  "model_score": 0.6175,
  "style_score": 0.7108,
  "label": "We cannot tell whether this was written by a person or by AI, so we are not making a call either way. This is not an accusation and it does not count against you. If you want it looked at by a person, you can ask.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "703ea4e7b6f4",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.8074,
  "model_score": 0.7387,
  "style_score": 0.9104,
  "label": "We think this was very likely written by AI. If you wrote it yourself, you can say so and a person will look at it. Nothing is decided until a person has.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "af6da737f822",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.8498,
  "model_score": 0.8051,
  "style_score": 0.9169,
  "label": "We think this was very likely written by AI. If you wrote it yourself, you can say so and a person will look at it. Nothing is decided until a person has.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "bc2f034f337e",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.8439,
  "model_score": 0.8329,
  "style_score": 0.8604,
  "label": "We think this was very likely written by AI. If you wrote it yourself, you can say so and a person will look at it. Nothing is decided until a person has.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "56e0646eda98",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.8684,
  "model_score": 0.8005,
  "style_score": 0.9703,
  "label": "We think this was very likely written by AI. If you wrote it yourself, you can say so and a person will look at it. Nothing is decided until a person has.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "986cf766d566",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.7793,
  "model_score": 0.8814,
  "style_score": 0.6261,
  "label": "We think this was very likely written by AI. If you wrote it yourself, you can say so and a person will look at it. Nothing is decided until a person has.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "7b4e875119d2",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.5508,
  "model_score": 0.8816,
  "style_score": 0.3727,
  "label": "We cannot tell whether this was written by a person or by AI, so we are not making a call either way. This is not an accusation and it does not count against you. If you want it looked at by a person, you can ask.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_FP08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "83b85b0bf55e",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4231,
  "model_score": 0.4625,
  "style_score": 0.364,
  "label": "We cannot tell whether this was written by a person or by AI, so we are not making a call either way. This is not an accusation and it does not count against you. If you want it looked at by a person, you can ask.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "30c6e2af165d",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2102,
  "model_score": 0.2044,
  "style_score": 0.2189,
  "label": "This reads like your own writing to us, and there is nothing further you need to do.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "c39ea34be639",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.6511,
  "model_score": 0.5943,
  "style_score": 0.7364,
  "label": "We cannot tell whether this was written by a person or by AI, so we are not making a call either way. This is not an accusation and it does not count against you. If you want it looked at by a person, you can ask.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "b2fb74ae4fa7",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5624,
  "model_score": 0.4998,
  "style_score": 0.6563,
  "label": "We cannot tell whether this was written by a person or by AI, so we are not making a call either way. This is not an accusation and it does not count against you. If you want it looked at by a person, you can ask.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "249f3f3a005c",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5953,
  "model_score": 0.6401,
  "style_score": 0.5282,
  "label": "We cannot tell whether this was written by a person or by AI, so we are not making a call either way. This is not an accusation and it does not count against you. If you want it looked at by a person, you can ask.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "14952b6a852a",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.6265,
  "model_score": 0.5583,
  "style_score": 0.7289,
  "label": "We cannot tell whether this was written by a person or by AI, so we are not making a call either way. This is not an accusation and it does not count against you. If you want it looked at by a person, you can ask.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "657acf7302bc",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.9586,
  "model_score": 0.9976,
  "style_score": 0.9,
  "label": "We think this was very likely written by AI. If you wrote it yourself, you can say so and a person will look at it. Nothing is decided until a person has.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "074bc141182f",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.6739,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "We cannot tell whether this was written by a person or by AI, so we are not making a call either way. This is not an accusation and it does not count against you. If you want it looked at by a person, you can ask.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
