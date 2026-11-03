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
## 1. My own writing is rarely called AI

<!-- Your criterion. It must name a number. -->

Of 10 pieces I wrote myself, at most 1 is labeled high-confidence AI, in each of the 3 trials.

**Why this target:**

On a writing site, wrong accusation costs a real writer much more than a missed detection costs the site. I write in English as a second language, which is exactly the kind of writing signal one tends to score as AI, so this is a hard target, not an easy one.

---

## 2. Clearly AI and clearly human text score far apart

<!-- Your criterion. -->

The combined score for the class `clearly_ai` sample is at least 0.35 higher than for the `clearly_human` sample, in each of the 3 trials.

**Why this target:**

If the two signals can't separate the most obvious cases, their judgment on anything in between means nothing. 0.35 is more than the width of my unsure band, so the two can't both land in it.

---

## 3. All three labels are reachable

<!-- Your criterion. -->

Among 6 test texts (2 clearly AI, 2 clearly human, 2 borderline), each of the three labels (human, unsure, AI) appears at least once, in each of the 3 trials.

**Why this target:**

A label no score can produce means my thresholds are wrong. Writers would only ever see two of the three messages I wrote.

---

## 4. Every appeal is recorded

<!-- Your criterion. -->

5 of 5 appeals against real `content_id`s return success and add an `under_review` entry to the log. An appeal with a `content_id` that doesn't exist returns 404 and adds nothing to the log.

**Why this target:**

The appeal is the only protection a wrongly accused writer has, so it can't fail even once. A typo in the `content_id` should give a clear error, not fail silently.

---

## 5. Bad input never crashes the service

<!-- Your criterion. -->

4 of 4 bad requests (no `text` field, empty text, `text` set to null, and text of 50,000 words) return a 4xx error with a JSON message, never a 500. `/ping` still answers afterward.

**Why this target:**

Crashing on malformed input is one of the most common real failures, and the next unit's attack set will try it. A writer who sends something wrong should be told what went wrong.

---

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
