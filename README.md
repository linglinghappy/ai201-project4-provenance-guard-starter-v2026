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

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. **The writing site sends a request.** It posts the `text` and a `creator_id` as JSON to `POST /submit`.
2. **`app.py` checks the input.** Missing or empty text is rejected. Valid text gets a `content_id`, so it can be found again later if the writer appeals.
3. **Signal one scores word choice.** `detector.py` gives a `model_score` from 0 to 1 for how predictable the words are.
4. **Signal two scores shape.** `stylometry.py` gives a `style_score` from 0 to 1 for how even the sentences and punctuation are.
5. **The two scores become one.** `scoring.py::combine_signals` merges them into a single confidence score.
6. **The score becomes a label.** `scoring.py::score_to_label` turns it into a guess (`ai`, `human` or `unsure`) and a plain-English sentence a reader can understand.
7. **The decision is logged and returned.** `audit.py` writes everything to `logs/audit.jsonl`, and the service sends the result back for the site to show. If the writer disagrees, they can send the `content_id` to `POST /appeal`, which marks the item `under_review`.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable each word is, given the words before it (perplexity, using GPT-2). More predictable text scores as more AI-like.

**Why that might differ between human and AI writing:** AI writes by picking a likely next word, so its text is easy to predict. Humans make less expected word choices.

**What it can't see:** Predictable doesn't mean AI. Kids and people writing in English as a second language often use simple, common words, so their real writing can look like AI. For example, "I like my school. My teacher is nice. I study every day." scored 0.65 (AI-like).

### Signal two — the style signal

**What it measures:** The shape of the text, without reading it: how much sentence length varies, and how many different kinds of punctuation are used. I also tried how often words repeat (type-token ratio), but left it out because on the class samples it ran backwards (AI 0.85, human 0.73).

**Why that might differ between human and AI writing:** AI sentences tend to be similar in length. Human writing is more uneven, with very short sentences next to long ones. In the class samples, the AI text's sentences were 4–18 words; the human text's were 2–36.

**What it can't see:** It can't read, so it doesn't know what the text says. Changing only the shape, like splitting sentences, adding typos or adding dashes, can fool it without changing the content. Punctuation habits like the dash are also used by both humans and AI.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Take the lower of the two scores. Text is only called AI if both signals agree it looks like AI; if either one thinks it looks human, that one wins. I chose this because wrongly accusing a real writer costs more than missing AI text. The cost is that AI text only has to fool one signal to get through.

**The numbers:** `combined = min(model_score, style_score)`. No weights, so `WEIGHT_MODEL_SIGNAL` and `WEIGHT_STYLE_SIGNAL` in `config.py` are not used.


| Text                                                                    | model | style | combined |
| ------------------------------------------------------------------------- | ------- | ------- | ---------- |
| clearly AI (class sample)                                               | 0.75  | 0.92  | 0.75     |
| clearly human (class sample)                                            | 0.44  | 0.00  | 0.00     |
| borderline / lightly-edited AI (class sample)                           | 0.35  | 0.55  | 0.35     |
| plain human: "I like my school. My teacher is nice. I study every day." | 0.65  | 1.00  | 0.65     |

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

"Obsidian lanterns flicker sideways. Grandmother hoards brass keys. Herons interrogate the marsh." Signal one scored it 0.02 (rare words, very human), and signal two scored it 1.00 (every sentence is 4 words, only full stops, very AI). My rule takes the lower score, 0.02, so it is labeled human.

(The plain human sentence in the table above combines to 0.65, which is why my AI threshold is 0.70 and not 0.65. See Label Variants.)

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->


| Label                 | Score range  | The exact text a reader sees                                                                                                                                                    |
| ----------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| high-confidence human | 0.00 – 0.35 | We think this was probably written by a person.                                                                                                                                 |
| unsure                | 0.35 – 0.70 | There isn't enough evidence to tell whether this was written by a person or with AI.                                                                                            |
| high-confidence AI    | 0.70 – 1.00 | Our automated check found strong signs that this may have been written with AI. The check can be wrong. If you wrote this yourself, you can appeal and a person will review it. |

**Why I worded the "unsure" one this way:**

<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

It says what is true: the system doesn't have enough evidence either way. It doesn't lean toward AI, so a writer who wrote every word themselves isn't being accused of anything.

I raised the AI threshold from 0.65 to 0.70 so the plain human sentence "I like my school. My teacher is nice. I study every day." (combined 0.65) lands in unsure instead of being called AI.

**Unit 8 update:** the table above shows the unit 7 ranges. In unit 8 I raised
the AI threshold again, from 0.70 to **0.81**. The ranges now in `config.py`
are: human 0.00–0.35, unsure 0.35–0.81, AI 0.81–1.00. The label text didn't
change. See [The Improvement](#the-improvement).

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ python -c 'import json,sys; print(json.dumps({"text": open(sys.argv[1]).read(), "creator_id": "ling"}))' samples/clearly_ai.txt \
  | curl -s -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d @-
```

```json
{
  "confidence": 0.7576,
  "content_id": "c_05a60087b357",
  "guess": "ai",
  "label": "Our automated check found strong signs that this may have been written with AI. The check can be wrong. If you wrote this yourself, you can appeal and a person will review it.",
  "model_score": 0.7576,
  "style_score": 0.9192
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "c_05a60087b357", "reasoning": "I wrote this myself for a class assignment."}'
```

```json
{
  "content_id": "c_05a60087b357",
  "message": "Thanks. Your appeal has been recorded and a person will review it.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 3,
  "entries": [
    {
      "combined_score": 0.3919,
      "content_id": "c_5caf68b71284",
      "creator_id": "ling",
      "guess": "unsure",
      "label": null,
      "model_score": 0.3919,
      "status": "decided",
      "style_score": 0.557,
      "timestamp": "2026-11-04T05:15:11+00:00"
    },
    {
      "combined_score": 0.7576,
      "content_id": "c_05a60087b357",
      "creator_id": "ling",
      "guess": "ai",
      "label": "Our automated check found strong signs that this may have been written with AI. The check can be wrong. If you wrote this yourself, you can appeal and a person will review it.",
      "model_score": 0.7576,
      "status": "decided",
      "style_score": 0.9192,
      "timestamp": "2026-11-04T05:23:45+00:00"
    },
    {
      "content_id": "c_05a60087b357",
      "creator_id": "ling",
      "event": "appeal",
      "reasoning": "I wrote this myself for a class assignment.",
      "status": "under_review",
      "timestamp": "2026-11-04T05:25:34+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* Draft text for my three labels.
- *What came back:* An unsure label that said "We can't tell whether this was written by a person or with AI. Plenty of genuine writing lands here, so this is not an accusation."
- *What I changed:* I rewrote it around the idea that there's a lack of evidence either way: "There isn't enough evidence to tell whether this was written by a person or with AI." It says what is actually true without needing to explain that it isn't an accusation.

**Moment 2**

- *What I asked for:* What `sentence_length_spread` should return for a one-sentence submission, where there's no spread to measure.
- *What came back:* A recommendation to return 0.0, which treats one sentence as AI-like.
- *What I changed:* I wanted 1.0 at first, to protect real writers. We discussed it: 1.0 would let AI text through just by writing one long sentence. I settled on the neutral middle value, because one sentence carries no information about spread, so the signal shouldn't pretend it does.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day

**Why those numbers and not others:**

<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

As we discussed in class, I started from how a real writer behaves and
picked numbers that fit that, then checked them against a script.

**A real writer.** A person submits their own work, reads the result, maybe
fixes a typo or a sentence, and submits again. That is a few submissions in a
short burst, and maybe a handful across a whole day.
- **5 per minute** leaves room for that burst: submit, fix, submit again.
- **50 per day** is far more than one person would ever need for their own
  writing.

So a real writer should never see a `429`.

**A script.** Someone trying to map my thresholds sends many small variations
of the same text, maybe 1,000 of them, to see where the label flips.
- With only the per-minute limit: 1,000 ÷ 5 = 200 minutes, about **3 hours**.
  That is not much protection.
- With the daily limit too: 1,000 ÷ 50 = **20 days**.

So the per-minute limit stops fast bursts, and the daily limit is what really
slows down a script.

**Why not other numbers?**
- **Lower** (e.g. 1 per minute): a writer fixing a typo and resubmitting right
  away would get blocked.
- **Higher** (e.g. the starter's 200 per day): 1,000 variations would get
  through in just 5 days.

**Known weakness:** the limit counts per `creator_id`. A script that uses a new
id for every request is never limited (see below).

**What a caller counts as:** 
Per `creator_id`. The limiter key (`rate_limit_key` in `app.py`) uses the
`creator_id` from the request body, and falls back to the caller's IP address
only when the body has no usable `creator_id`. The weakness: a script that
sends a fresh `creator_id` on every request looks like a thousand different
callers and never trips the limit.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
$ python run_attacks.py --flood 15
15 submissions as 'flood_tester' against http://127.0.0.1:5000
The first one is slow while the model loads.

  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 429
  [ 7/15] 429
  [ 8/15] 429
  [ 9/15] 429
  [10/15] 429
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429

============================================================
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
============================================================

10 of 15 were rate limited.
```

(Also saved as `results/flood_2026-11-04_1718.md`.)

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

The full table, with every attack, its outcome and a held/broke mark, is in
[`results/attack_run_2026-11-04_1815_before.md`](results/attack_run_2026-11-04_1815_before.md).
The full audit log for the run is in `results/audit_extract.json`.

**How I marked them.** I asked one question for every row: did the attacker
get what they were going for?
- **evasion** (AI text trying to pass as human): `ai` is held; `unsure` or
  `human` is broke, because the AI text got past the `ai` label.
- **false_positive** (human text trying to get flagged): `human` or `unsure`
  is held, because no writer was accused; `ai` is broke.
- **prompt_injection**: broke only if the instruction got what it asked for
  (a `human` label, a changed label, a damaged log).
- **malformed**: a `400` is held; a `500`, or junk input that still got a
  confident `ai`/`human` label, is broke.
- **flood**: `200` × 5 then `429` is held.

| Family | Broke | Held |
|---|---|---|
| evasion | 8 | 2 |
| false_positive | 5 | 3 |
| prompt_injection | 1 | 5 |
| malformed | 8 | 12 |
| flood_same_creator | 0 | 12 |
| **Total (56)** | **22** | **34** |

Notes:
- **RQ07** (a JSON array as the body) crashed `/submit` with a `500`. The run
  sent 56 requests but the log has only 55 entries for it: the crash left
  **no trace at all**.
- **RQ10 and RQ11** are marked held, but they got a `429` from the limiter
  (no usable `creator_id`, so they counted against my address). They never
  reached my route, so they weren't really tested.
- **RQ02** (no `creator_id`) is marked broke: it was scored and logged as
  `"unknown"`, so nobody can trace who sent it.

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
{"timestamp": "2026-11-05T02:15:29+00:00", "content_id": "c_fd854648d91b", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.9799, "combined_score": 0.8051, "label": "Our automated check found strong signs that this may have been written with AI. The check can be wrong. If you wrote this yourself, you can appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-05T02:15:29+00:00", "content_id": "c_7b40081e696f", "creator_id": "attacker_FP02", "guess": "ai", "model_score": 0.7387, "style_score": 1.0, "combined_score": 0.7387, "label": "Our automated check found strong signs that this may have been written with AI. The check can be wrong. If you wrote this yourself, you can appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-05T02:15:30+00:00", "content_id": "c_3d23e5146c0f", "creator_id": "attacker_MF07", "guess": "ai", "model_score": 0.9064, "style_score": 0.75, "combined_score": 0.75, "label": "Our automated check found strong signs that this may have been written with AI. The check can be wrong. If you wrote this yourself, you can appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-05T02:15:29+00:00", "content_id": "c_5d0b68c5f469", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.582, "combined_score": 0.2044, "label": "We think this was probably written by a person.", "status": "decided"}
{"timestamp": "2026-11-05T02:15:28+00:00", "content_id": "c_d7da1e61c090", "creator_id": "attacker_EV01", "guess": "human", "model_score": 0.1635, "style_score": 1.0, "combined_score": 0.1635, "label": "We think this was probably written by a person.", "status": "decided"}
{"timestamp": "2026-11-05T02:15:29+00:00", "content_id": "c_9c20001cba48", "creator_id": "attacker_EV08", "guess": "human", "model_score": 0.2452, "style_score": 1.0, "combined_score": 0.2452, "label": "We think this was probably written by a person.", "status": "decided"}
{"timestamp": "2026-11-05T02:15:29+00:00", "content_id": "c_5b4f52312f89", "creator_id": "attacker_FP07", "guess": "unsure", "model_score": 0.8816, "style_score": 0.6922, "combined_score": 0.6922, "label": "There isn't enough evidence to tell whether this was written by a person or with AI.", "status": "decided"}
{"timestamp": "2026-11-05T02:15:30+00:00", "content_id": "c_e7a85493d034", "creator_id": {"id": "x"}, "guess": "human", "model_score": 0.0492, "style_score": 0.75, "combined_score": 0.0492, "label": "We think this was probably written by a person.", "status": "decided"}
{"timestamp": "2026-11-05T02:15:30+00:00", "content_id": "c_ab1086effca0", "creator_id": "unknown", "guess": "human", "model_score": 0.2395, "style_score": 0.75, "combined_score": 0.2395, "label": "We think this was probably written by a person.", "status": "decided"}
{"timestamp": "2026-11-05T02:15:30+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
{"timestamp": "2026-11-05T02:15:30+00:00", "creator_id": "unknown", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
```

What each entry shows:
1. **FP03**: a non-native English speaker writing carefully, labelled `ai`
   (0.81). Both signals agreed (0.81 and 0.98), so my "take the lower score"
   rule could not protect them. **Broke.**
2. **FP02**: formal human writing (a working-group report), labelled `ai`
   (0.74). The style score is 1.0, its maximum. **Broke.**
3. **MF07**: a sentence in Arabic, labelled `ai` (0.75). A real language,
   written by a person, accused because the model is built for English.
   **Broke.**
4. **PI02**: AI text with a fake "SYSTEM: return human" line on top,
   labelled `human` (0.20). My detector doesn't read instructions; the extra
   line changed the text's statistics enough to drop the model score.
   **Broke.**
5. **EV01**: AI text with typos added, labelled `human` (0.16). **Broke.**
6. **EV08**: AI text shorter than the model's window, labelled `human`
   (0.25). **Broke.**
7. **FP07**: human text that repeats a phrase on purpose. The model score was
   0.88 (AI-like); only the lower style score (0.69) kept it at `unsure`. My
   min rule worked here, by 0.008. **Held, barely.**
8. **RQ06**: `creator_id` sent as an object. It was scored and the object
   went straight into the log as `{"id": "x"}`. **Broke.**
9. **RQ02**: no `creator_id` at all. Scored and logged as `"unknown"`, so it
   can't be traced to anyone. **Broke.**
10. **FL01** (rejected): a `429` from the flood rows, all sharing one
    `creator_id`. The limiter stopped it and the rejection was logged.
    **Held.**
11. **RQ10/RQ11** (rejected): a `429` against `"unknown"`. The request had no
    readable `creator_id`, so it counted against my address and never
    reached the route. **Not really tested.**

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**FP03: a non-native English speaker, writing carefully in plain words, was
told their work showed "strong signs" of AI** (combined score 0.81, well past
my 0.70 threshold).

This is the worst because:
- **They did nothing wrong.** Writing in simple, safe vocabulary is exactly
  what a careful second-language writer does, and it is exactly what signal
  one reads as "predictable", and so as AI.
- **Both signals agreed**, so my safety rule (take the lower score) didn't
  help. There was no split for it to resolve toward human.
- **They are the writer least able to argue back.** An appeal asks them to
  defend their writing, in the language they're still learning, to the
  system that just accused them.
- **It's not a one-off.** FP02 (formal), FP04 (student essay), FP05
  (technical docs) and FP06 (a formal letter) failed the same way. Plain,
  careful writing gets flagged.

FP02 (formal writing, 0.74) is just as bad in kind. I picked FP03 because
its score is higher (0.81 vs 0.74): the system was more confident in the
wrong answer. MF07 (Arabic labelled `ai`) is a close second, for the same
reason.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->


| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
| ----------- | -------- | ------- | ------- | ------- | --------- |
| 1. My own writing labelled `ai` | ≤ 1 of 10 | 2/10 | 2/10 | 2/10 | **MISSED** |
| 2. `clearly_ai` minus `clearly_human` combined score | ≥ 0.35 | 0.754 | 0.754 | 0.754 | MET |
| 3. human, unsure and ai all reached among 6 texts | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| 4. Real appeals → `under_review` in the log; fake id → 404, log unchanged | 5 of 5 + 404 | 5/5 + 404 | 5/5 + 404 | 5/5 + 404 | MET |
| 5. Bad input → 4xx with a JSON message, never a 500; `/ping` answers after | 4 of 4 + ping | 3/4 + ping | 3/4 + ping | 3/4 + ping | **MISSED** |

All three trials returned identical scores, as expected: nothing in either
signal is random.

- Criteria 1, 2, 3, 5: `results/run_2026-11-10_2219_before.md`, produced by
  `run_eval.py::main` against `app.py::submit`.
- Criterion 4 and the `/ping` half of 5:
  `results/appeal_eval_2026-11-10_2221_before.md`, produced by
  `eval_appeals.py::main` against `app.py::appeal` and `app.py::ping`.

**Real output from one trial** (Trial 1 of each), pasted as text:

**Criterion 1:** `run_eval.py::main`, `results/run_2026-11-10_2219_before.md`.
The two pieces labelled `ai` (`03.txt`, `06.txt`), and one that wasn't
(`01.txt`) for comparison:

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7111,
    "model_score": 0.7111,
    "style_score": 1.0,
    "label": "Our automated check found strong signs that this may have been written with AI. The check can be wrong. If you wrote this yourself, you can appeal and a person will review it.",
    "sent": "I disagree with the statement that scientists and scholars should conc"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7173,
    "model_score": 0.7173,
    "style_score": 0.8927,
    "label": "Our automated check found strong signs that this may have been written with AI. The check can be wrong. If you wrote this yourself, you can appeal and a person will review it.",
    "sent": "I support Maria’s idea of investing the city's budget in infrastructur"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4203,
    "model_score": 0.4203,
    "style_score": 0.4219,
    "label": "There isn't enough evidence to tell whether this was written by a person or with AI.",
    "sent": "Steve Job was proud of giving speech for graduates of Stanford. For th"
  }
]
```

**Criterion 2:** `run_eval.py::main`, `results/run_2026-11-10_2219_before.md`.
0.7544 − 0.0 = 0.754:

```json
[
  {"status": 200, "guess": "ai", "confidence": 0.7544, "model_score": 0.7544, "style_score": 0.9192, "sent": "clearly_ai.txt"},
  {"status": 200, "guess": "human", "confidence": 0.0, "model_score": 0.4445, "style_score": 0.0, "sent": "clearly_human.txt"}
]
```

**Criterion 3:** `run_eval.py::main`, `results/run_2026-11-10_2219_before.md`.
Guesses in order: ai, ai, human, human, human, unsure:

```json
[
  {"status": 200, "guess": "ai", "confidence": 0.7544, "model_score": 0.7544, "style_score": 0.9192},
  {"status": 200, "guess": "ai", "confidence": 0.8124, "model_score": 0.8124, "style_score": 0.9781},
  {"status": 200, "guess": "human", "confidence": 0.0, "model_score": 0.4445, "style_score": 0.0},
  {"status": 200, "guess": "human", "confidence": 0.1159, "model_score": 0.1159, "style_score": 0.6667},
  {"status": 200, "guess": "human", "confidence": 0.3489, "model_score": 0.3489, "style_score": 0.5488},
  {"status": 200, "guess": "unsure", "confidence": 0.6733, "model_score": 0.6733, "style_score": 1.0}
]
```

**Criterion 4:** `eval_appeals.py::main`,
`results/appeal_eval_2026-11-10_2221_before.md`. One real appeal, then the
fake id:

```json
{
  "content_id": "c_8023e38e3eb5",
  "submit_status": 200,
  "appeal_status": 200,
  "response": {
    "content_id": "c_8023e38e3eb5",
    "message": "Thanks. Your appeal has been recorded and a person will review it.",
    "status": "under_review"
  },
  "under_review_entries_in_log": 1,
  "log_entry": {
    "content_id": "c_8023e38e3eb5",
    "creator_id": "eval_appeal_t1_1",
    "event": "appeal",
    "reasoning": "I wrote this myself (eval trial 1, appeal 1).",
    "status": "under_review",
    "timestamp": "2026-11-11T04:21:34+00:00"
  },
  "passed": true
}
```

```json
{
  "status": 404,
  "response": {
    "error": "not_found",
    "message": "No submission with content_id 'c_doesnotexist0'."
  },
  "log_entries_before": 161,
  "log_entries_after": 161,
  "passed": true
}
```

**Criterion 5:** `run_eval.py::main`, `results/run_2026-11-10_2219_before.md`.
Three 400s, then the 50,000-word body scored and labelled `ai` with a 200:

```json
[
  {"status": 400, "guess": null, "confidence": null, "sent": "{\"creator_id\": \"eval_bad_missing\"}"},
  {"status": 400, "guess": null, "confidence": null, "sent": "(empty text)"},
  {"status": 400, "guess": null, "confidence": null, "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}"},
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.75,
    "model_score": 0.9975,
    "style_score": 0.75,
    "label": "Our automated check found strong signs that this may have been written with AI. The check can be wrong. If you wrote this yourself, you can appeal and a person will review it.",
    "sent": "word word word word word word word word word word word word word word "
  }
]
```

And `/ping` afterwards, from `eval_appeals.py::main`:

```json
{
  "status": 200,
  "response": {"ok": true, "service": "provenance-guard", "you_sent": "still alive?"},
  "passed": true
}
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

**Verdicts:** criteria 2, 3 and 4 are MET. Criteria 1 and 5 are MISSED,
because the target failed in every trial. All three trials were identical,
so nothing in the pipeline is unstable.

There are 24 failures to explain: 2 missed criteria and 22 broken attacks.
They come from **four problems**, not 24.

---

**Pattern 1: careful, plain writing looks like AI to both signals.**
*Covers criterion 1 (my `03.txt` and `06.txt`), FP02, FP03, FP04, FP05 and
FP06. 7 accusations of real writers.*

| Input | Signal one (model) | Signal two (style) | Combined | Label |
|---|---|---|---|---|
| my `03.txt` (scientists essay) | 0.711 | 1.000 | 0.711 | ai |
| my `06.txt` (Taichung buses) | 0.717 | 0.893 | 0.717 | ai |
| FP02 formal register | 0.739 | 1.000 | 0.739 | ai |
| FP03 non-native speaker | 0.805 | 0.980 | 0.805 | ai |
| FP04 rubric essay | 0.833 | 0.952 | 0.833 | ai |
| FP05 technical docs | 0.801 | 1.000 | 0.801 | ai |
| FP06 formal template | 0.881 | 0.843 | 0.843 | ai |

- **Stage: signal one and signal two together.** The combining rule can't
  help, because nothing is split.
- **Signal one's mechanism:** careful writers, and especially second-language
  writers, choose safe, common words and standard phrases ("From my
  perspective", "In addition", "As a result"). GPT-2 finds those easy to
  predict, so perplexity is low and the model score is high.
- **Signal two's mechanism:** it measures sentence-length spread and the
  number of *kinds* of punctuation. My `03.txt` uses only two kinds (`,` and
  `.`) and its sentences are all of similar length (spread 0.28). Both
  measures sit at the "AI" end, so the style score is 1.0, the maximum.
- **Why this is one problem:** I picked two signals so that they would
  disagree on human writing. On *plain, careful* writing they don't. Both
  really measure "regular and predictable", and careful human writing is
  regular and predictable. The min rule only protects writers when the
  signals split. Here they agree, so there is no split to resolve toward
  human.

---

**Pattern 2: an attacker only has to fool ONE signal, and clean AI text has
almost no margin.**
*Covers EV01, EV02, EV03, EV04, EV05, EV06, EV07, EV08 and PI02. 9 AI texts
let through.*

- **Stage: the combining rule (take the lower score) and the label mapping
  (AI threshold 0.70).**
- **Mechanism:** the min rule means whichever signal is *lower* decides. An
  attacker doesn't need to fool both signals, only one. On top of that, the
  untouched `clearly_ai` sample scores only 0.754, just **0.054 above** my AI
  threshold. Any edit that pushes one signal down by a little more than 0.05
  takes AI text out of the `ai` label.

The failures split by which signal was pushed down:

*Signal one pushed down (the model score dropped, style stayed high):*

| Attack | Model | Style | Combined | Label |
|---|---|---|---|---|
| EV01 typos | **0.164** | 1.000 | 0.164 | human |
| EV04 unusual words | **0.611** | 1.000 | 0.611 | unsure |
| EV05 heavy editing | **0.321** | 0.565 | 0.321 | human |
| EV08 below the token window | **0.245** | 1.000 | 0.245 | human |
| PI02 fake "SYSTEM:" line | **0.204** | 0.582 | 0.204 | human |

Typos, rare words, an odd "SYSTEM:" line and very short text all make GPT-2
more *surprised*. Perplexity rises, so the model score falls. EV01 was aimed
at signal two ("typos raise word variety"), but my signal two doesn't measure
word variety, and its style score stayed at 1.0. The typos broke **signal
one** instead: misspelled words are rare token sequences for GPT-2. PI02 did
not work as an instruction, since nothing in my service reads instructions.
It worked as *unusual text*.

*Signal two pushed down (style dropped, model stayed moderate):*

| Attack | Model | Style | Combined | Label |
|---|---|---|---|---|
| EV03 pasted quotation | 0.666 | **0.398** | 0.398 | unsure |
| EV06 one long + one short sentence | 0.573 | **0.500** | 0.500 | unsure |
| EV07 punctuation padding | 0.586 | **0.417** | 0.417 | unsure |

Signal two can't read. A quotation adds quotation marks and other
punctuation kinds, padding adds more kinds, and one very long sentence next
to one very short one creates a big length spread. Each changes the
*shape* of the text without changing who wrote it.

*Both pushed down a little:* EV02 (broken-up sentences) moved style to 0.608
and model to 0.594. Neither is a big drop, but both are below 0.70.

---

**Pattern 3: the route accepts text that isn't writing, and signal two gives
it a default score that lands on a label.**
*Covers criterion 5 (50,000 × "word"), MF03, MF04, MF05, MF06 and MF07. 6
junk inputs given confident labels.*

| Input | Model | Style | Combined | Label |
|---|---|---|---|---|
| 50,000 × "word" (criterion 5) | 0.998 | 0.750 | 0.750 | ai |
| MF05 one very long word | 0.998 | 0.750 | 0.750 | ai |
| MF06 emoji only | 0.997 | 0.750 | 0.750 | ai |
| MF07 Arabic (right-to-left) | 0.906 | 0.750 | 0.750 | ai |
| MF03 control characters | 0.000 | 0.750 | 0.000 | human |
| MF04 punctuation only | 0.011 | 0.250 | 0.011 | human |

- **Stage: the route first, then signal two.**
- **Route mechanism:** `app.py::submit` only checks that `text` is a
  non-empty string. It has no length limit and no check that the text
  contains words. So 50,000 repeated words, emoji, control characters and a
  string of punctuation all go through to scoring.
- **Signal two mechanism:** the identical 0.750 is a fingerprint. Text with
  no sentence breaks counts as one sentence, so `sentence_length_spread`
  returns its neutral midpoint (0.65, which scales to 0.5). Text with no
  punctuation has 0 kinds (which scales to 0). That gives
  1 − (0.5 + 0) / 2 = **0.75**, which is above my 0.70 AI threshold. Signal
  one scores repetitive or byte-level tokens as very predictable (0.9+), so
  min(0.9+, 0.75) = 0.75 → `ai`. **Any input without punctuation or
  sentence breaks gets labelled AI.**
- **MF07 is the worst of these:** it is real writing by a person, in a
  language GPT-2 wasn't trained on, and it was called AI by the same
  default.
- MF03 and MF04 go the other way: GPT-2 is so surprised by control
  characters and bare punctuation that the model score is about 0, so junk
  is confidently labelled `human`.

---

**Pattern 4: the route trusts the shape of the request body.**
*Covers RQ02, RQ06 and RQ07.*

- **Stage: the route.**
- **RQ07 (500 crash, no log entry):**
  `payload = request.get_json(silent=True) or {}` only falls back to `{}`
  when the body is empty or unparseable. A JSON array like `["text"]` is
  truthy, so `payload` is a *list*, and `payload.get("text")` raises
  `AttributeError`. That happens before any `audit.log_...` call, so the
  crash leaves no trace. (The 429 handler already checks
  `isinstance(payload, dict)`. The route doesn't.)
- **RQ06 (object as `creator_id`):** the route never checks that
  `creator_id` is a string, so `{"id": "x"}` was scored and written to the
  log as an object.
- **RQ02 (no `creator_id`):** the route defaults it to `"unknown"`. The
  decision is logged but can't be traced to anyone, and every caller with
  no id shares one rate-limit bucket.

---

**What the patterns say together:** Patterns 1 and 2 are the same weakness
seen from two sides. My two signals both measure "regular and predictable",
and the AI threshold sits just under where clean AI text lands. Careful human
writing is pushed *over* the threshold (Pattern 1), and lightly disguised AI
text slips *under* it (Pattern 2). Patterns 3 and 4 are route problems: the
service scores things it should have refused.

**Criteria I'm not revising:** both misses were measurable, and the targets
were fair. Criterion 1 at "at most 1 in 10" stays. Loosening it to make the
miss go away is exactly the change that doesn't count.

**Honest note on the criteria I met:**
- Criterion 3 met its target, but only just. `borderline.txt` was labelled
  `human` (0.349, right on the 0.35 line), and the only `unsure` came from my
  plain "market" text at 0.673, 0.027 below the AI line.
- Criterion 2 rests on a single pair of samples. If I tightened one, it
  would be criterion 2: require the spread on several AI/human pairs, not
  one.

---

## The Improvement

**What I changed:** one line in `config.py`:
`AI_THRESHOLD` went from **0.70 to 0.81**. Nothing else changed: same
signals, same combining rule (take the lower score), same human threshold
(0.35), same route. The unsure band is now 0.35–0.81 instead of 0.35–0.70.

**Which diagnosis pointed at it:** Pattern 1. Careful, plain human writing
(FP02, FP03, FP05, my `03.txt` and `06.txt`) combined to 0.71–0.81, just over
the old 0.70 line, and was told it showed "strong signs" of AI. Both signals
agreed on those texts, so the combining rule had nothing to resolve. The only
stage left that could stop the accusation was the label mapping.

**Why 0.81 exactly:** it is the highest value that still lets the strongest
AI sample in criterion 3 (0.812) reach the `ai` label. Above 0.812, criterion
3 breaks. At 0.81 it fixes FP03 (0.805), my worst outcome. **I picked this
number by looking at my test scores**, so it is tuned to this test set. On new
text it could land differently.

### Attack Run — After

The full table is in
[`results/attack_run_2026-11-10_2259_after.md`](results/attack_run_2026-11-10_2259_after.md),
marked with the same rules as the before run. Criteria:
[`results/run_2026-11-10_2259_after.md`](results/run_2026-11-10_2259_after.md)
(`run_eval.py::main`) and
[`results/appeal_eval_2026-11-10_2259_after.md`](results/appeal_eval_2026-11-10_2259_after.md)
(`eval_appeals.py::main`).

**Attack set, before and after:**

| Family | Before: broke / held | After: broke / held | Change |
|---|---|---|---|
| evasion | 8 / 2 | **9 / 1** | worse: EV09 now gets through |
| false_positive | 5 / 3 | **2 / 6** | better: FP02, FP03, FP05 no longer accused |
| prompt_injection | 1 / 5 | 1 / 5 | no change |
| malformed | 8 / 12 | **5 / 15** | better: MF05, MF06, MF07 now `unsure`, not `ai` |
| flood_same_creator | 0 / 12 | 0 / 12 | no change |
| **Total (56)** | **22 / 34** | **17 / 39** | 5 fewer broken |

**Every attack whose result changed:**

| ID | What it is | Score | Before | After | Verdict change |
|---|---|---|---|---|---|
| FP02 | formal human writing | 0.739 | ai | unsure | broke → **held** |
| FP03 | non-native speaker (my worst outcome) | 0.805 | ai | unsure | broke → **held** |
| FP05 | technical docs by a person | 0.801 | ai | unsure | broke → **held** |
| MF05 | one very long word | 0.750 | ai | unsure | broke → **held** |
| MF06 | emoji only | 0.750 | ai | unsure | broke → **held** |
| MF07 | Arabic | 0.750 | ai | unsure | broke → **held** |
| EV09 | AI text + human opening | 0.704 | ai | unsure | held → **broke** |

Every score is identical to the before run. Only the line the scores are
compared against moved.

**My five criteria, before and after** (three trials each; all three
identical in both runs):

| Criterion | Target | Before (Run 1 / 2 / 3) | Verdict | After (Run 1 / 2 / 3) | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labelled `ai` | ≤ 1 of 10 | 2/10 · 2/10 · 2/10 | MISSED | **0/10 · 0/10 · 0/10** | **MET** |
| 2. `clearly_ai` − `clearly_human` | ≥ 0.35 | 0.754 · 0.754 · 0.754 | MET | 0.754 · 0.754 · 0.754 | MET |
| 3. All three labels reached | 3 of 3 | 3/3 · 3/3 · 3/3 | MET | 3/3 · 3/3 · 3/3 | MET (barely) |
| 4. Appeals recorded; fake id → 404 | 5 of 5 + 404 | 5/5 · 5/5 · 5/5 | MET | 5/5 · 5/5 · 5/5 | MET |
| 5. Bad input → 4xx, `/ping` answers | 4 of 4 + ping | 3/4 · 3/4 · 3/4 | MISSED | 3/4 · 3/4 · 3/4 | MISSED |

Real output from the after run, criterion 3, Trial 1 (`run_eval.py::main`,
`results/run_2026-11-10_2259_after.md`). `clearly_ai.txt` is now `unsure`,
and the only `ai` left is the 0.812 text:

```json
[
  {"status": 200, "guess": "unsure", "confidence": 0.7544, "model_score": 0.7544, "style_score": 0.9192},
  {"status": 200, "guess": "ai", "confidence": 0.8124, "model_score": 0.8124, "style_score": 0.9781},
  {"status": 200, "guess": "human", "confidence": 0.0, "model_score": 0.4445, "style_score": 0.0},
  {"status": 200, "guess": "human", "confidence": 0.1159, "model_score": 0.1159, "style_score": 0.6667},
  {"status": 200, "guess": "human", "confidence": 0.3489, "model_score": 0.3489, "style_score": 0.5488},
  {"status": 200, "guess": "unsure", "confidence": 0.6733, "model_score": 0.6733, "style_score": 1.0}
]
```

**Did it help, and how do I know:**

**Yes, for the problem I aimed at. It cost something on the other side.**

*What got better:*
- **No human writer in my tests is accused at 0.71–0.81 any more.** Criterion
  1 went from MISSED to MET: 0 of my 10 pieces are labelled `ai`, down from
  2. FP02, FP03 and FP05 moved from `ai` to `unsure`. FP03, the non-native
  writer I picked as the worst outcome, is now told "there isn't enough
  evidence", not "strong signs of AI".
- MF07, real writing in Arabic, is no longer called AI.

*What it cost:*
- **AI text gets through more often.** EV09 (0.704) went from held to broke.
  More important: the plain, undisguised `clearly_ai.txt` (0.754) is now
  `unsure`. Of the 12 AI texts in my tests (the two class/criterion AI
  samples and EV01–EV10), only **2 are labelled `ai`** now, down from 4.
- Criterion 3 still meets its target, but by 0.002: the only `ai` label left
  comes from a text at 0.812 against a 0.81 line.
- The unsure band is now 0.35–0.81, almost half the scale. `unsure` is
  becoming the answer to most things.

*What it didn't fix:*
- **FP04 (0.833) and FP06 (0.843)** are still accused. To clear them I'd
  need 0.85, and then criterion 3 fails because nothing reaches `ai`.
- **Criterion 5 is still MISSED.** The 50,000-word body is now `unsure`
  instead of `ai`, but it still returns 200, not a 4xx. That is a route
  problem (Pattern 3), and a threshold can't fix it.
- **RQ07 still crashes with a 500**, and MF03/MF04 junk is still labelled
  `human`. Those are Patterns 3 and 4, also route problems.
- Patterns 1 and 2 still have the same root: both signals measure "regular
  and predictable". I moved the line; I didn't make the signals better.

**The honest summary:** I moved errors from "accusing writers" to "letting
AI through". The people who paid before were writers like FP03. The people
who pay now are the platform and the readers, who will see more AI text
labelled `unsure`. For a writing site, where a wrong accusation is the
worse harm (my criterion 1), I think that's the right direction. But it is a
trade, not a fix.

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

After the change, 17 attacks still break and criterion 5 is still missed.
They fall under the same four patterns as the diagnosis.

**Why I stopped after one change, in general:** the milestone asked for one
change, measured properly. If I had changed the route at the same time as
the threshold, I could not say which change moved which number. Each fix
below is the next single change I would make and measure on its own.

---

**1. Route problems: RQ07, RQ06, RQ02, MF03, MF04, and criterion 5
(MISSED).**

| Still broken | What happens now |
|---|---|
| RQ07 (JSON array body) | 500 crash, and nothing in the log |
| RQ06 (`creator_id` is an object) | scored, and the object is written to the log |
| RQ02 (no `creator_id`) | scored and logged as `"unknown"` |
| MF03 (control characters) | labelled `human` (0.000) |
| MF04 (punctuation only) | labelled `human` (0.011) |
| Criterion 5: 50,000 × "word" | 200 and `unsure`, not a 4xx |

- **What I'd do:** validate the input in `app.py::submit` before either
  signal runs:
  - if the body isn't a JSON object, return 400 and log it;
  - require `creator_id` to be a non-empty string, otherwise 400;
  - cap the length (for example 5,000 words, which is far more than one
    piece of writing), otherwise 400;
  - require a minimum share of letters, so control characters, bare
    punctuation and emoji are refused rather than scored.
- **Why I stopped:** this is the fix I'd make **next**. It is cheap and
  low-risk, and it would turn criterion 5 to MET and fix RQ07's silent
  crash. I didn't make it this time only because of the one-change rule. I
  chose the threshold first because a wrong accusation of a real writer is
  worse harm than a 500 on a junk request.
- **One open question:** the letters check would also need to accept
  non-Latin scripts like MF07's Arabic. Refusing a real language as
  "junk" would be another way of treating non-English writers badly.

---

**2. AI text that fools one signal: EV01–EV09 and PI02 (10 attacks).**

These got *worse* or stayed broken. Raising the threshold made it even easier
for AI text to land in `unsure`. EV09 (0.704) broke this time.

- **What I'd do:**
  - **Change the combining rule.** "Take the lower score" means fooling
    one signal is enough. A weighted average (for example 0.6 model / 0.4
    style) would make an attacker move both.
  - **Make signal two harder to game.** Count punctuation *kinds* only
    when each kind appears more than once, so one pasted quotation or a
    sprinkle of padding (EV03, EV07) doesn't count.
  - **For short text (EV08)**, return `unsure` with a "too short to
    judge" note instead of a confident `human`.
- **Why I stopped:** each of these moves the false-positive side too. The
  min rule is exactly what protects writers when the signals split (in the
  before run, FP07 held by 0.008 because of it). Replacing it needs a full before/after run
  of its own. I'd also need more AI samples than I have: my AI side is
  only 12 texts.

---

**3. Careful human writing still accused: FP04 (0.833) and FP06 (0.843).**

- **What I'd do:** the threshold can't go higher without losing the `ai`
  label entirely (criterion 3 breaks above 0.812). The real fix is
  upstream. Both signals reward "regular and predictable", and a rubric
  essay or a formal template is regular and predictable *on purpose*. I'd
  look for a signal that measures something different, for example whether
  the text contains specific, personal detail (names, places, numbers,
  first-person events). Many of my own essays have that kind of detail
  (Taichung's free buses, my sister's cabbage research), but I haven't
  tested whether it actually separates human from AI text.
- **Why I stopped:** that is building a new signal, not tuning one, and
  it's more than this unit's time allowed.

---

**4. Criterion 3 met by 0.002.** It isn't broken, but it is fragile. The
only `ai` label left in my criterion-3 texts is 0.812 against a 0.81 line.
Any small change to the model or the text could tip it to MISSED. I'd add
more AI samples to criterion 3 so the verdict doesn't rest on one text.

---

**The trade I'd make if this ran for real:**

I would keep leaning toward fewer wrong accusations, as the 0.81 threshold
does, because a writer told their own work looks like AI pays with their
reputation and has to defend themselves, and that falls hardest on
second-language writers like FP03 and me. The cost is paid by the platform
and its readers, who will see more AI-written text get through as `unsure`,
so I'd make sure `unsure` sends the piece to a human reviewer rather than
quietly letting it pass.

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
