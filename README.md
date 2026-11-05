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
| 1.        |        |       |       |       |         |
| 2.        |        |       |       |       |         |
| 3.        |        |       |       |       |         |
| 4.        |        |       |       |       |         |
| 5.        |        |       |       |       |         |

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
