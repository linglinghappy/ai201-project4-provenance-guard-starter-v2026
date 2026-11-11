# Appeal and /ping check — before

- Produced by: `eval_appeals.py::main` (criterion 4, and /ping for criterion 5)
- Service: `app.py::appeal`, `app.py::ping` · log: `audit.py::log_appeal`
- 3 trials · 2026-11-10 22:21

| Check | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Real appeals recorded as under_review | 5/5 | 5/5 | 5/5 |
| Fake content_id → 404, log unchanged | yes | yes | yes |
| /ping answers after bad input | yes | yes | yes |

## What actually came back

### Trial 1

```json
{
  "trial": 1,
  "appeals": [
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
    },
    {
      "content_id": "c_95ac0ff0f2a1",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_95ac0ff0f2a1",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_95ac0ff0f2a1",
        "creator_id": "eval_appeal_t1_2",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 1, appeal 2).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:21:34+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_6977bb3ac9f3",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_6977bb3ac9f3",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_6977bb3ac9f3",
        "creator_id": "eval_appeal_t1_3",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 1, appeal 3).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:21:34+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_5234f0fa2794",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_5234f0fa2794",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_5234f0fa2794",
        "creator_id": "eval_appeal_t1_4",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 1, appeal 4).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:21:34+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_e643196cc550",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_e643196cc550",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_e643196cc550",
        "creator_id": "eval_appeal_t1_5",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 1, appeal 5).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:21:34+00:00"
      },
      "passed": true
    }
  ],
  "fake": {
    "status": 404,
    "response": {
      "error": "not_found",
      "message": "No submission with content_id 'c_doesnotexist0'."
    },
    "log_entries_before": 161,
    "log_entries_after": 161,
    "passed": true
  },
  "ping": {
    "status": 200,
    "response": {
      "ok": true,
      "service": "provenance-guard",
      "you_sent": "still alive?"
    },
    "passed": true
  }
}
```

### Trial 2

```json
{
  "trial": 2,
  "appeals": [
    {
      "content_id": "c_1b544a4c93fa",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_1b544a4c93fa",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_1b544a4c93fa",
        "creator_id": "eval_appeal_t2_1",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 2, appeal 1).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:21:35+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_e386bd04b75c",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_e386bd04b75c",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_e386bd04b75c",
        "creator_id": "eval_appeal_t2_2",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 2, appeal 2).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:21:35+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_ae1dbf1b4fb4",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_ae1dbf1b4fb4",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_ae1dbf1b4fb4",
        "creator_id": "eval_appeal_t2_3",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 2, appeal 3).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:21:35+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_c03568e48d97",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_c03568e48d97",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_c03568e48d97",
        "creator_id": "eval_appeal_t2_4",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 2, appeal 4).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:21:35+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_95bc40ad1db4",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_95bc40ad1db4",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_95bc40ad1db4",
        "creator_id": "eval_appeal_t2_5",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 2, appeal 5).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:21:35+00:00"
      },
      "passed": true
    }
  ],
  "fake": {
    "status": 404,
    "response": {
      "error": "not_found",
      "message": "No submission with content_id 'c_doesnotexist0'."
    },
    "log_entries_before": 175,
    "log_entries_after": 175,
    "passed": true
  },
  "ping": {
    "status": 200,
    "response": {
      "ok": true,
      "service": "provenance-guard",
      "you_sent": "still alive?"
    },
    "passed": true
  }
}
```

### Trial 3

```json
{
  "trial": 3,
  "appeals": [
    {
      "content_id": "c_dbec617ade5b",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_dbec617ade5b",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_dbec617ade5b",
        "creator_id": "eval_appeal_t3_1",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 3, appeal 1).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:21:35+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_c81d3c2de3b8",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_c81d3c2de3b8",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_c81d3c2de3b8",
        "creator_id": "eval_appeal_t3_2",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 3, appeal 2).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:21:35+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_1c67ff58b5de",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_1c67ff58b5de",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_1c67ff58b5de",
        "creator_id": "eval_appeal_t3_3",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 3, appeal 3).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:21:35+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_25c76b0bae5d",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_25c76b0bae5d",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_25c76b0bae5d",
        "creator_id": "eval_appeal_t3_4",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 3, appeal 4).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:21:35+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_63a4f4ab08cb",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_63a4f4ab08cb",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_63a4f4ab08cb",
        "creator_id": "eval_appeal_t3_5",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 3, appeal 5).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:21:35+00:00"
      },
      "passed": true
    }
  ],
  "fake": {
    "status": 404,
    "response": {
      "error": "not_found",
      "message": "No submission with content_id 'c_doesnotexist0'."
    },
    "log_entries_before": 189,
    "log_entries_after": 189,
    "passed": true
  },
  "ping": {
    "status": 200,
    "response": {
      "ok": true,
      "service": "provenance-guard",
      "you_sent": "still alive?"
    },
    "passed": true
  }
}
```
