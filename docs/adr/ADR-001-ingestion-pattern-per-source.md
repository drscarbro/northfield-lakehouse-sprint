# ADR-001: Auto Loader for clickstream and orders, scheduled batch for inventory

## Status

Proposed

## Date

2026-09-08

## Context

Northfield Commerce has three source feeds landing in cloud storage before anything touches Bronze: clickstream events (high-volume, continuously-arriving JSON), an orders extract (append/update mix, arrives as a CDC-style feed), and an inventory snapshot (one file per warehouse per day). Treating all three the same way — either "everything is a scheduled batch job" or "everything is a stream" — is the default a less experienced pipeline gets built with, and it's wrong in both directions here: batching clickstream loses freshness the funnel-metrics use case needs, and streaming inventory adds operational complexity a once-a-day snapshot doesn't justify.

## Decision Drivers

- Freshness requirement differs by source: clickstream feeds a near-real-time funnel view (Week 4); inventory only needs to be current as of "this morning."
- Schema stability differs: clickstream event shapes evolve as new event types ship; inventory's schema is fixed by the warehouse system's export format.
- Operational cost: a continuously-running stream has a cluster-hours cost that a once-daily batch job doesn't.
- File arrival pattern: clickstream and orders arrive as many small files continuously; inventory arrives as one file per warehouse, once a day.

## Options Considered

### Option A: Auto Loader (streaming) for all three sources

- Pros: one ingestion pattern to operate and monitor; lowest possible latency across the board.
- Cons: pays continuous cluster cost for a source (inventory) that only changes once a day; adds checkpoint/state management overhead with no corresponding benefit.

### Option B: Scheduled batch (e.g. a nightly `COPY INTO` or full-file read) for all three sources

- Pros: simplest operational model; no streaming checkpoints to manage.
- Cons: clickstream freshness drops to the batch interval, which breaks the Week 4 real-time funnel requirement; at clickstream's file-arrival volume, repeatedly listing and re-scanning the source directory in batch mode is more expensive than incremental file discovery.

### Option C: Auto Loader for clickstream and orders, scheduled batch for inventory

- Pros: matches ingestion cost and complexity to each source's actual freshness need; Auto Loader's incremental file listing (rather than full directory scan) is the right fit for clickstream and orders' continuous small-file arrival; inventory's single-file-per-day pattern gets no benefit from streaming infrastructure.
- Cons: two ingestion code paths to maintain instead of one; requires being explicit, in code and in this document, about which sources get which treatment so the split doesn't look accidental.

## Decision

Northfield Commerce ingests clickstream and orders with Auto Loader (`cloudFiles`, schema evolution on, rescued-data column enabled) and ingests inventory with a scheduled daily batch read. The split is driven by freshness requirement and file-arrival pattern, not by a blanket "streaming is more modern" preference — Option C is the only one of the three where every source's ingestion cost is justified by an actual downstream requirement.

## Evidence

- [ ] TODO: Auto Loader file-discovery latency for clickstream, measured from file landing to Bronze commit (target: p95 under 2 minutes).
- [ ] TODO: Cost comparison — Auto Loader continuous job cluster-hours/day for clickstream+orders vs. what a naive "stream everything" config would have cost with inventory included.
- [ ] TODO: Link to the Auto Loader notebook / DLT source definitions once built.
- [ ] TODO: Screenshot of the schema evolution event log after the first upstream clickstream schema change (this is the moment that actually proves schema evolution was worth turning on).

## Consequences

### Positive

- Ingestion cost and operational complexity are proportional to each source's actual freshness need.
- The rescued-data column on the streaming sources means a malformed event doesn't fail the pipeline or silently disappear.

### Negative / trade-offs accepted

- Two ingestion patterns means two things to monitor and two runbooks, not one.
- If inventory's business requirement changes (e.g., real-time stock levels for the storefront), this decision needs to be revisited, not just the code.

### Follow-ups

- If a fourth source arrives, evaluate it against these same drivers rather than defaulting to whichever pattern is already used elsewhere in the pipeline.

## Related

- Feeds directly into ADR-002 (Silver/Gold layout) and the Week 4 streaming funnel work, which depends on clickstream's Auto Loader latency being low enough to be meaningfully "real-time."
