#!/usr/bin/env python3
"""
Criterion 4 (appeals) and the /ping half of criterion 5, three trials.

run_eval.py only sends /submit, so it can't test an appeal: an appeal needs a
submission first, then an appeal against the content_id that came back. This
script does that, the same three-trial way.

    python app.py                                  # in one terminal
    python eval_appeals.py --label before          # in another

Criterion 4: 5 of 5 appeals against real content_ids return success and add an
under_review entry to the log. An appeal with a content_id that doesn't exist
returns 404 and adds nothing to the log.

Criterion 5 (second half): after the bad-input requests, /ping still answers.

It only sends requests and records what came back. It changes nothing in the
service.
"""

import argparse
import datetime as dt
import json
import sys

import requests

import config
import scenarios

DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"

APPEAL_TEXTS = [
    "I walked to the market this morning and bought some apples. The weather was "
    "cold, but the sun came out later. I talked to the old man who sells bread.",
    "The importance of effective time management cannot be overstated in today's "
    "fast-paced work environment. Clear priorities help teams meet deadlines.",
    "Grandma kept her buttons in a tin that once held Danish cookies. The lid stuck; "
    "you had to pry it with a butter knife, swearing quietly.",
    "We got to the campsite about four. The pitch was fine, a bit sloped, but there "
    "was a tap nearby and the toilets were clean enough.",
    "Artificial intelligence is transforming many industries. It offers significant "
    "benefits, including increased efficiency and improved decision-making.",
]
FAKE_ID = "c_doesnotexist0"


def log_entries(url):
    return requests.get(f"{url}/log", params={"limit": 100000}, timeout=30).json()["entries"]


def run_trial(url, trial):
    out = {"trial": trial, "appeals": [], "fake": None, "ping": None}

    # Criterion 4: five real appeals.
    for i, text in enumerate(APPEAL_TEXTS, 1):
        creator = f"eval_appeal_t{trial}_{i}"
        sub = requests.post(f"{url}/submit", json={"text": text, "creator_id": creator},
                            timeout=90)
        content_id = sub.json().get("content_id")
        resp = requests.post(f"{url}/appeal", json={
            "content_id": content_id,
            "reasoning": f"I wrote this myself (eval trial {trial}, appeal {i}).",
        }, timeout=30)
        logged = [e for e in log_entries(url)
                  if e.get("content_id") == content_id and e.get("status") == "under_review"]
        ok = resp.status_code == 200 and resp.json().get("status") == "under_review" \
            and len(logged) == 1
        out["appeals"].append({
            "content_id": content_id, "submit_status": sub.status_code,
            "appeal_status": resp.status_code, "response": resp.json(),
            "under_review_entries_in_log": len(logged),
            "log_entry": logged[-1] if logged else None, "passed": ok,
        })

    # Criterion 4: an appeal against an id that doesn't exist.
    before = len(log_entries(url))
    resp = requests.post(f"{url}/appeal", json={
        "content_id": FAKE_ID, "reasoning": "This id was never issued.",
    }, timeout=30)
    after = len(log_entries(url))
    out["fake"] = {
        "status": resp.status_code, "response": resp.json(),
        "log_entries_before": before, "log_entries_after": after,
        "passed": resp.status_code == 404 and before == after,
    }

    # Criterion 5, second half: send the bad-input bodies, then /ping.
    bad = next(s for s in scenarios.SCENARIOS if s.get("criterion") == 5)
    for body in bad["bodies"]:
        try:
            requests.post(f"{url}/submit", json=body, timeout=90)
        except Exception:  # noqa: BLE001 — a crash here is what /ping checks for
            pass
    try:
        ping = requests.post(f"{url}/ping", json={"message": "still alive?"}, timeout=10)
        out["ping"] = {"status": ping.status_code, "response": ping.json(),
                       "passed": ping.status_code == 200 and ping.json().get("ok") is True}
    except Exception as exc:  # noqa: BLE001
        out["ping"] = {"status": None, "error": f"{type(exc).__name__}: {exc}",
                       "passed": False}
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    args = parser.parse_args()

    try:
        requests.get(f"{args.url}/health", timeout=5)
    except Exception:  # noqa: BLE001
        sys.exit(f"Nothing answering at {args.url}. Start it:  python app.py")

    trials = []
    for t in range(1, args.trials + 1):
        r = run_trial(args.url, t)
        trials.append(r)
        n_ok = sum(a["passed"] for a in r["appeals"])
        print(f"trial {t}: appeals {n_ok}/5 · fake id "
              f"{'404, log unchanged' if r['fake']['passed'] else 'FAILED'} · "
              f"/ping {'ok' if r['ping']['passed'] else 'FAILED'}")

    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"appeal_eval_{stamp}{label}.md"

    lines = [
        f"# Appeal and /ping check{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `eval_appeals.py::main` (criterion 4, and /ping for criterion 5)",
        "- Service: `app.py::appeal`, `app.py::ping` · log: `audit.py::log_appeal`",
        f"- {args.trials} trials · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "| Check | " + " | ".join(f"Run {t['trial']}" for t in trials) + " |",
        "|---|" + "---|" * len(trials),
        "| Real appeals recorded as under_review | "
        + " | ".join(f"{sum(a['passed'] for a in t['appeals'])}/5" for t in trials) + " |",
        "| Fake content_id → 404, log unchanged | "
        + " | ".join("yes" if t["fake"]["passed"] else "no" for t in trials) + " |",
        "| /ping answers after bad input | "
        + " | ".join("yes" if t["ping"]["passed"] else "no" for t in trials) + " |",
        "",
        "## What actually came back",
        "",
    ]
    for t in trials:
        lines += [f"### Trial {t['trial']}", "", "```json",
                  json.dumps(t, indent=2, ensure_ascii=False), "```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
