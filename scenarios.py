"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

from pathlib import Path

_SAMPLES = Path(__file__).parent / "samples"


def _sample(name: str) -> str:
    return (_SAMPLES / name).read_text(encoding="utf-8").strip()


def _my_writing() -> list[str]:
    """
    Criterion 1: ten pieces I wrote myself, one per file in samples/my_writing/
    (01.txt ... 10.txt). A missing file shows up as a placeholder, so
    validate() refuses to run until all ten are there.
    """
    folder = _SAMPLES / "my_writing"
    texts = []
    for i in range(1, 11):
        f = folder / f"{i:02d}.txt"
        texts.append(f.read_text(encoding="utf-8").strip() if f.exists()
                     else f"REPLACE ME: samples/my_writing/{i:02d}.txt is missing")
    return texts


SCENARIOS = [
    {
        # Criterion 1 — target: at most 1 of 10 labelled "ai", in every trial.
        "name": "my own writing",
        "criterion": 1,
        "texts": _my_writing(),
    },
    {
        # Criterion 2 — target: clearly_ai's combined score is at least 0.35
        # higher than clearly_human's, in every trial.
        "name": "score spread",
        "criterion": 2,
        "texts": [
            _sample("clearly_ai.txt"),
            _sample("clearly_human.txt"),
        ],
    },
    {
        # Criterion 3 — target: human, unsure and ai each appear at least once
        # among these 6, in every trial. Order: 2 AI, 2 human, 2 borderline.
        "name": "label coverage",
        "criterion": 3,
        "texts": [
            _sample("clearly_ai.txt"),
            "Artificial intelligence is transforming many industries. It offers "
            "significant benefits, including increased efficiency and improved "
            "decision-making. However, it also raises important ethical considerations.",
            _sample("clearly_human.txt"),
            "Grandma kept her buttons in a tin that once held Danish cookies \u2014 a "
            "cruel trick on every grandchild. The lid stuck; you had to pry it with a "
            "butter knife, swearing quietly.",
            _sample("borderline.txt"),
            "I walked to the market this morning and bought some apples. The weather "
            "was cold, but the sun came out later. I talked to the old man who sells bread.",
        ],
    },
    # Criterion 4 (appeals) can't be expressed as texts or bodies: it needs a
    # submission first, then an appeal against the content_id that came back.
    # It is tested by eval_appeals.py instead, three trials, same as here.
    {
        # Criterion 5 — target: 4 of 4 return a 4xx with a JSON message, never
        # a 500. (/ping afterwards is checked by eval_appeals.py.)
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"creator_id": "eval_bad_missing"},               # no text field
            {"text": "", "creator_id": "eval_bad_empty"},     # empty text
            {"text": None, "creator_id": "eval_bad_null"},    # text is null
            {"text": "word " * 50000, "creator_id": "eval_bad_huge"},  # 50,000 words
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
