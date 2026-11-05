# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-04 18:15
- Auto-marked BROKE (5xx, crash, no response): **1**
- Left for you to judge: **55**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.


| ID      | Family             | Targeting                                              | Status | Content ID       | Guess  | Score | Verdict |
| --------- | -------------------- | -------------------------------------------------------- | -------- | ------------------ | -------- | ------- | --------- |
| EV01    | evasion            | signal two: typos raise word variety                   | 200    | `c_d7da1e61c090` | human  | 0.164 | broke   |
| EV02    | evasion            | signal two: broken-up sentences raise length spread    | 200    | `c_252301743581` | unsure | 0.594 | broke   |
| EV03    | evasion            | signal two: a pasted quotation changes the shape       | 200    | `c_dae2e228ddc0` | unsure | 0.398 | broke   |
| EV04    | evasion            | signal one: unusual words raise perplexity             | 200    | `c_2c4a6dbc945e` | unsure | 0.611 | broke   |
| EV05    | evasion            | both signals: heavy human editing pass                 | 200    | `c_d55575fd1d78` | human  | 0.321 | broke   |
| EV06    | evasion            | signal two: one very long sentence and one very short  | 200    | `c_a0283591d67c` | unsure | 0.500 | broke   |
| EV07    | evasion            | signal two: padding with punctuation                   | 200    | `c_1d7f26a9ce6e` | unsure | 0.417 | broke   |
| EV08    | evasion            | signal one: text below the token window                | 200    | `c_9c20001cba48` | human  | 0.245 | broke   |
| EV09    | evasion            | both: AI text with a human opening paragraph bolted on | 200    | `c_ee43faa8e0c6` | ai     | 0.704 | held    |
| EV10    | evasion            | signal two: repeated stanza structure                  | 200    | `c_36231770780a` | ai     | 0.933 | held    |
| FP01    | false_positive     | plain, clear human writing with no flourishes          | 200    | `c_495d261f21b7` | unsure | 0.618 | held    |
| FP02    | false_positive     | human writing in a formal register                     | 200    | `c_7b40081e696f` | ai     | 0.739 | broke   |
| FP03    | false_positive     | a non-native English speaker writing carefully         | 200    | `c_fd854648d91b` | ai     | 0.805 | broke   |
| FP04    | false_positive     | a student essay written to a rubric                    | 200    | `c_5c268e0b22a0` | ai     | 0.833 | broke   |
| FP05    | false_positive     | technical documentation written by a person            | 200    | `c_2d3df632f255` | ai     | 0.800 | broke   |
| FP06    | false_positive     | a person imitating a formal template                   | 200    | `c_42bcaf75018e` | ai     | 0.843 | broke   |
| FP07    | false_positive     | human writing that repeats a phrase deliberately       | 200    | `c_5b4f52312f89` | unsure | 0.692 | held    |
| FP08    | false_positive     | very short genuine human submission                    | 200    | `c_316f2aba965e` | human  | 0.322 | held    |
| PI01    | prompt_injection   | instruction to ignore the check                        | 200    | `c_3c34bde06688` | unsure | 0.463 | held    |
| PI02    | prompt_injection   | instruction disguised as a system message              | 200    | `c_5d0b68c5f469` | human  | 0.204 | broke   |
| PI03    | prompt_injection   | instruction wrapped in the writer's voice              | 200    | `c_70c789f566b4` | unsure | 0.594 | held    |
| PI04    | prompt_injection   | attempt to make the label text hostile                 | 200    | `c_7d6dd04b158e` | unsure | 0.500 | held    |
| PI05    | prompt_injection   | attempt to inject into the audit log                   | 200    | `c_37f652f409ef` | unsure | 0.544 | held    |
| PI06    | prompt_injection   | instruction plus real human text                       | 200    | `c_e86e275cce72` | unsure | 0.558 | held    |
| MF01    | malformed          | text is only whitespace                                | 400    | `—`             | —     | —    | held    |
| MF02    | malformed          | text is a single character                             | 400    | `—`             | —     | —    | held    |
| MF03    | malformed          | text is control characters                             | 200    | `c_255546a4b450` | human  | 0.000 | broke   |
| MF04    | malformed          | text is only punctuation                               | 200    | `c_4e22d7ae2fef` | human  | 0.011 | broke   |
| MF05    | malformed          | text is a very long single word                        | 200    | `c_e1c85d29eecc` | ai     | 0.750 | broke   |
| MF06    | malformed          | text is emoji only                                     | 200    | `c_f091e1cdbccf` | ai     | 0.750 | broke   |
| MF07    | malformed          | text is right-to-left script                           | 200    | `c_3d23e5146c0f` | ai     | 0.750 | broke   |
| MF08    | malformed          | text is 60,000 characters                              | 200    | `c_d6f42b3324fd` | ai     | 0.908 | held    |
| RQ01    | malformed          | no text field at all                                   | 400    | `—`             | —     | —    | held    |
| RQ02    | malformed          | no creator_id                                          | 200    | `c_ab1086effca0` | human  | 0.239 | broke   |
| RQ03    | malformed          | text is a number                                       | 400    | `—`             | —     | —    | held    |
| RQ04    | malformed          | text is a list                                         | 400    | `—`             | —     | —    | held    |
| RQ05    | malformed          | text is null                                           | 400    | `—`             | —     | —    | held    |
| RQ06    | malformed          | creator_id is an object                                | 200    | `c_e7a85493d034` | human  | 0.049 | broke   |
| RQ07    | malformed          | body is a JSON array, not an object                    | 500    | `—`             | —     | —    | broke   |
| RQ08    | malformed          | body is unparseable JSON                               | 400    | `—`             | —     | —    | held    |
| RQ09    | malformed          | body is empty                                          | 400    | `—`             | —     | —    | held    |
| RQ10    | malformed          | body is form-encoded, not JSON                         | 429    | `—`             | —     | —    | held    |
| RQ11    | malformed          | body is JSON claiming to be plain text                 | 429    | `—`             | —     | —    | held    |
| RQ12    | malformed          | deeply nested JSON                                     | 400    | `—`             | —     | —    | held    |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `c_23f5d37e9c4b` | human  | 0.029 | held |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `c_fa39ec35b891` | human  | 0.029 | held |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `c_eded0c4c7503` | human  | 0.029 | held |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `c_831b784e98ef` | human  | 0.029 | held |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `c_9dc19fc0eea3` | human  | 0.029 | held |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator                  | 429    | `—`             | —     | —    | held |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator                  | 429    | `—`             | —     | —    | held |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator                  | 429    | `—`             | —     | —    | held |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator                  | 429    | `—`             | —     | —    | held |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator                  | 429    | `—`             | —     | —    | held |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator                  | 429    | `—`             | —     | —    | held |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator                  | 429    | `—`             | —     | —    | held |

---

## By family


| Family               | Attacks | Auto-BROKE | Left to judge |
| ---------------------- | --------- | ------------ | --------------- |
| `evasion`            | 10      | 0          | 10            |
| `false_positive`     | 8       | 0          | 8             |
| `flood_same_creator` | 12      | 0          | 12            |
| `malformed`          | 20      | 1          | 19            |
| `prompt_injection`   | 6       | 0          | 6             |

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
  "content_id": "c_d7da1e61c090",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.1635,
  "model_score": 0.1635,
  "style_score": 1.0,
  "label": "We think this was probably written by a person.",
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
  "content_id": "c_252301743581",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5943,
  "model_score": 0.5943,
  "style_score": 0.6077,
  "label": "There isn't enough evidence to tell whether this was written by a person or with AI.",
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
  "content_id": "c_dae2e228ddc0",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.3976,
  "model_score": 0.6662,
  "style_score": 0.3976,
  "label": "There isn't enough evidence to tell whether this was written by a person or with AI.",
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
  "content_id": "c_2c4a6dbc945e",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6114,
  "model_score": 0.6114,
  "style_score": 1.0,
  "label": "There isn't enough evidence to tell whether this was written by a person or with AI.",
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
  "content_id": "c_d55575fd1d78",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3212,
  "model_score": 0.3212,
  "style_score": 0.5653,
  "label": "We think this was probably written by a person.",
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
  "content_id": "c_a0283591d67c",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.5727,
  "style_score": 0.5,
  "label": "There isn't enough evidence to tell whether this was written by a person or with AI.",
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
  "content_id": "c_1d7f26a9ce6e",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4167,
  "model_score": 0.5862,
  "style_score": 0.4167,
  "label": "There isn't enough evidence to tell whether this was written by a person or with AI.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "c_9c20001cba48",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.2452,
  "model_score": 0.2452,
  "style_score": 1.0,
  "label": "We think this was probably written by a person.",
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
  "content_id": "c_ee43faa8e0c6",
  "creator_id": "attacker_EV09",
  "guess": "ai",
  "confidence": 0.7042,
  "model_score": 0.7042,
  "style_score": 0.8804,
  "label": "Our automated check found strong signs that this may have been written with AI. The check can be wrong. If you wrote this yourself, you can appeal and a person will review it.",
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
  "content_id": "c_36231770780a",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.9329,
  "model_score": 0.9792,
  "style_score": 0.9329,
  "label": "Our automated check found strong signs that this may have been written with AI. The check can be wrong. If you wrote this yourself, you can appeal and a person will review it.",
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
  "content_id": "c_495d261f21b7",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.6175,
  "model_score": 0.6175,
  "style_score": 0.8875,
  "label": "There isn't enough evidence to tell whether this was written by a person or with AI.",
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
  "content_id": "c_7b40081e696f",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7387,
  "model_score": 0.7387,
  "style_score": 1.0,
  "label": "Our automated check found strong signs that this may have been written with AI. The check can be wrong. If you wrote this yourself, you can appeal and a person will review it.",
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
  "content_id": "c_fd854648d91b",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.8051,
  "model_score": 0.8051,
  "style_score": 0.9799,
  "label": "Our automated check found strong signs that this may have been written with AI. The check can be wrong. If you wrote this yourself, you can appeal and a person will review it.",
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
  "content_id": "c_5c268e0b22a0",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.8329,
  "model_score": 0.8329,
  "style_score": 0.9524,
  "label": "Our automated check found strong signs that this may have been written with AI. The check can be wrong. If you wrote this yourself, you can appeal and a person will review it.",
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
  "content_id": "c_2d3df632f255",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.8005,
  "model_score": 0.8005,
  "style_score": 1.0,
  "label": "Our automated check found strong signs that this may have been written with AI. The check can be wrong. If you wrote this yourself, you can appeal and a person will review it.",
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
  "content_id": "c_42bcaf75018e",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.8434,
  "model_score": 0.8814,
  "style_score": 0.8434,
  "label": "Our automated check found strong signs that this may have been written with AI. The check can be wrong. If you wrote this yourself, you can appeal and a person will review it.",
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
  "content_id": "c_5b4f52312f89",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.6922,
  "model_score": 0.8816,
  "style_score": 0.6922,
  "label": "There isn't enough evidence to tell whether this was written by a person or with AI.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "c_316f2aba965e",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.3223,
  "model_score": 0.3223,
  "style_score": 0.905,
  "label": "We think this was probably written by a person.",
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
  "content_id": "c_3c34bde06688",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4625,
  "model_score": 0.4625,
  "style_score": 0.7409,
  "label": "There isn't enough evidence to tell whether this was written by a person or with AI.",
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
  "content_id": "c_5d0b68c5f469",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2044,
  "model_score": 0.2044,
  "style_score": 0.582,
  "label": "We think this was probably written by a person.",
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
  "content_id": "c_70c789f566b4",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5943,
  "model_score": 0.5943,
  "style_score": 0.6359,
  "label": "There isn't enough evidence to tell whether this was written by a person or with AI.",
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
  "content_id": "c_7d6dd04b158e",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4998,
  "model_score": 0.4998,
  "style_score": 0.5976,
  "label": "There isn't enough evidence to tell whether this was written by a person or with AI.",
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
  "content_id": "c_37f652f409ef",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5442,
  "model_score": 0.6401,
  "style_score": 0.5442,
  "label": "There isn't enough evidence to tell whether this was written by a person or with AI.",
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
  "content_id": "c_e86e275cce72",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5583,
  "model_score": 0.5583,
  "style_score": 0.8961,
  "label": "There isn't enough evidence to tell whether this was written by a person or with AI.",
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
  "status": 200,
  "content_id": "c_255546a4b450",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.0,
  "model_score": 0.0,
  "style_score": 0.75,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "c_4e22d7ae2fef",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.0112,
  "model_score": 0.0112,
  "style_score": 0.25,
  "label": "We think this was probably written by a person.",
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
  "content_id": "c_e1c85d29eecc",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.75,
  "model_score": 0.9976,
  "style_score": 0.75,
  "label": "Our automated check found strong signs that this may have been written with AI. The check can be wrong. If you wrote this yourself, you can appeal and a person will review it.",
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
  "content_id": "c_f091e1cdbccf",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.75,
  "model_score": 0.9969,
  "style_score": 0.75,
  "label": "Our automated check found strong signs that this may have been written with AI. The check can be wrong. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "c_3d23e5146c0f",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.75,
  "model_score": 0.9064,
  "style_score": 0.75,
  "label": "Our automated check found strong signs that this may have been written with AI. The check can be wrong. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "c_d6f42b3324fd",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.9084,
  "model_score": 0.9876,
  "style_score": 0.9084,
  "label": "Our automated check found strong signs that this may have been written with AI. The check can be wrong. If you wrote this yourself, you can appeal and a person will review it.",
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
  "status": 200,
  "content_id": "c_ab1086effca0",
  "creator_id": null,
  "guess": "human",
  "confidence": 0.2395,
  "model_score": 0.2395,
  "style_score": 0.75,
  "label": "We think this was probably written by a person.",
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
  "status": 200,
  "content_id": "c_e7a85493d034",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.0492,
  "model_score": 0.0492,
  "style_score": 0.75,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 500,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>AttributeError: 'list' object has no attribute 'get'\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes",
  "verdict": "BROKE"
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
  "status": 429,
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
  "status": 429,
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
  "status": 200,
  "content_id": "c_23f5d37e9c4b",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0287,
  "model_score": 0.0287,
  "style_score": 0.75,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "c_fa39ec35b891",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0287,
  "model_score": 0.0287,
  "style_score": 0.75,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "c_eded0c4c7503",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0287,
  "model_score": 0.0287,
  "style_score": 0.75,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "c_831b784e98ef",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0287,
  "model_score": 0.0287,
  "style_score": 0.75,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "c_9dc19fc0eea3",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0287,
  "model_score": 0.0287,
  "style_score": 0.75,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
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

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
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

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
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
