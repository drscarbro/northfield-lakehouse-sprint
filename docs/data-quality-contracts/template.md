# Data Quality Contract: <table or pipeline stage>

Every DLT expectation (or equivalent check) on this table, as a contract — not just as code. If a field isn't in this table, it isn't being enforced, and that should be a deliberate choice, not an oversight.

| Field | Rule | Action on failure | Rationale |
|---|---|---|---|
| e.g. `order_id` | NOT NULL, unique | `expect_or_fail` (halt pipeline) | A duplicate or null order_id corrupts every downstream aggregate. |
| e.g. `event_timestamp` | not in the future | `expect_or_drop` (drop row, keep pipeline running) | Clock skew from a client happens; one bad event shouldn't halt ingestion. |
| | | | |

## Actions, defined

- **`expect_or_fail`**: halts the pipeline. Use only where a violation means downstream data is actively wrong, not just incomplete.
- **`expect_or_drop`**: drops the offending row, pipeline continues. Use where a violation means "this one record is bad," not "something upstream broke."
- **`expect` (log only)**: records the violation without changing pipeline behavior. Use for signals you're not yet confident enough in to gate on.

## Review

Revisit this contract whenever a new field is added to the table or a downstream consumer reports a data issue that this contract should have caught but didn't.
