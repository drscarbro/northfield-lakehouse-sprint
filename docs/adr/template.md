# ADR-NNN: <Short, decision-focused title>

Title it as the decision, not the topic — "Liquid Clustering over Z-Order for the orders fact table," not "Delta Lake performance."

## Status

`Proposed` | `Accepted` | `Superseded by ADR-NNN`

## Date

YYYY-MM-DD

## Context

What problem forced this decision? What was true about the system (data volume, query pattern, team constraint, exam-relevant requirement) that made the default choice not obviously correct? Two or three sentences — this section justifies why the ADR exists at all.

## Decision Drivers

The forces you're actually weighing, in priority order. Anyone reading only this list should be able to guess your decision before reading further.

- driver 1 (e.g., p99 query latency under 500ms)
- driver 2 (e.g., write throughput during nightly backfill)
- driver 3 (e.g., operational cost / cluster-hours)

## Options Considered

### Option A: <name>

- Pros:
- Cons:

### Option B: <name>

- Pros:
- Cons:

### Option C: <name> *(only if a real third option existed — don't pad this)*

- Pros:
- Cons:

## Decision

State the choice in one sentence, then justify it against the decision drivers above — not against the options' pros/cons list again. This is the paragraph an interviewer will actually read.

## Evidence

The thing that separates a real ADR from a guess. Link or paste:

- Benchmark numbers (before/after, with the query/workload that produced them)
- A notebook or script that reproduces the measurement
- A screenshot of the relevant metric (Spark UI, query history, cost dashboard)

If you wrote this ADR before you had evidence, mark it `Proposed` and come back to promote it to `Accepted` once you do. Don't backfill fake numbers.

## Consequences

### Positive

-

### Negative / trade-offs accepted

-

### Follow-ups

- What has to be revisited if data volume grows 10x, or if a new source appears?

## Related

- ADR-NNN (if this supersedes, depends on, or conflicts with another decision)
- Link to the relevant code, notebook, or pipeline file
