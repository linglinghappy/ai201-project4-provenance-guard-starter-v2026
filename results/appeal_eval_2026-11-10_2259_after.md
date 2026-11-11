# Appeal and /ping check — after

- Produced by: `eval_appeals.py::main` (criterion 4, and /ping for criterion 5)
- Service: `app.py::appeal`, `app.py::ping` · log: `audit.py::log_appeal`
- 3 trials · 2026-11-10 22:59

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
      "content_id": "c_046444969876",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_046444969876",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_046444969876",
        "creator_id": "eval_appeal_t1_1",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 1, appeal 1).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:59:29+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_dbf0a8e4f555",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_dbf0a8e4f555",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_dbf0a8e4f555",
        "creator_id": "eval_appeal_t1_2",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 1, appeal 2).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:59:29+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_302905756959",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_302905756959",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_302905756959",
        "creator_id": "eval_appeal_t1_3",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 1, appeal 3).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:59:29+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_33dc87e5f340",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_33dc87e5f340",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_33dc87e5f340",
        "creator_id": "eval_appeal_t1_4",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 1, appeal 4).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:59:29+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_c81a915ae368",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_c81a915ae368",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_c81a915ae368",
        "creator_id": "eval_appeal_t1_5",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 1, appeal 5).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:59:29+00:00"
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
    "log_entries_before": 324,
    "log_entries_after": 324,
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
      "content_id": "c_889b1237278c",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_889b1237278c",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_889b1237278c",
        "creator_id": "eval_appeal_t2_1",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 2, appeal 1).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:59:29+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_8e7f3894ba2b",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_8e7f3894ba2b",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_8e7f3894ba2b",
        "creator_id": "eval_appeal_t2_2",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 2, appeal 2).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:59:29+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_5b9ad222998e",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_5b9ad222998e",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_5b9ad222998e",
        "creator_id": "eval_appeal_t2_3",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 2, appeal 3).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:59:29+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_25a75fd25938",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_25a75fd25938",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_25a75fd25938",
        "creator_id": "eval_appeal_t2_4",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 2, appeal 4).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:59:29+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_b3d346b0aa5f",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_b3d346b0aa5f",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_b3d346b0aa5f",
        "creator_id": "eval_appeal_t2_5",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 2, appeal 5).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:59:29+00:00"
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
    "log_entries_before": 338,
    "log_entries_after": 338,
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
      "content_id": "c_eafe76a9784e",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_eafe76a9784e",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_eafe76a9784e",
        "creator_id": "eval_appeal_t3_1",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 3, appeal 1).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:59:29+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_2af43845d42b",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_2af43845d42b",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_2af43845d42b",
        "creator_id": "eval_appeal_t3_2",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 3, appeal 2).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:59:29+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_e2bc0fd845f1",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_e2bc0fd845f1",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_e2bc0fd845f1",
        "creator_id": "eval_appeal_t3_3",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 3, appeal 3).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:59:30+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_e4ddc0b10a94",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_e4ddc0b10a94",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_e4ddc0b10a94",
        "creator_id": "eval_appeal_t3_4",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 3, appeal 4).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:59:30+00:00"
      },
      "passed": true
    },
    {
      "content_id": "c_960ed67b2964",
      "submit_status": 200,
      "appeal_status": 200,
      "response": {
        "content_id": "c_960ed67b2964",
        "message": "Thanks. Your appeal has been recorded and a person will review it.",
        "status": "under_review"
      },
      "under_review_entries_in_log": 1,
      "log_entry": {
        "content_id": "c_960ed67b2964",
        "creator_id": "eval_appeal_t3_5",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 3, appeal 5).",
        "status": "under_review",
        "timestamp": "2026-11-11T04:59:30+00:00"
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
    "log_entries_before": 352,
    "log_entries_after": 352,
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
