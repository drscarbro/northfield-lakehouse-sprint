# ADR-002: Liquid Clustering vs. Z-Order for the orders fact table

## Status

Planned — due Week 2 (Sep 15–21)

## Date

TBD

## Context

The Gold-layer orders fact table needs a physical layout strategy that keeps both point-lookup queries (a single order by ID) and range-scan queries (all orders for a customer in a date range) fast as the table grows. Delta Lake offers two competing answers here — `OPTIMIZE` + `ZORDER BY`, and Liquid Clustering — and the Professional exam expects you to know the actual trade-off, not just that both exist.

## Decision Drivers

- Query pattern mix: point lookups vs. range scans on the orders fact table.
- Write pattern: this table receives continuous small-batch upserts from the Silver layer, not one-time bulk loads — clustering maintenance cost under continuous writes matters.
- Whether the clustering key needs to change over the table's life (Liquid Clustering allows this without a full rewrite; Z-Order does not).

## Options Considered

*(Fill in after benchmarking — don't pre-write the pros/cons list before you have the numbers.)*

### Option A: `OPTIMIZE` + `ZORDER BY`

- Pros:
- Cons:

### Option B: Liquid Clustering

- Pros:
- Cons:

## Decision

*(TODO — write this only after the Week 2 benchmark exists. State the choice in one sentence, justified against the decision drivers above.)*

## Evidence

- [ ] TODO: Benchmark query latency (point-lookup and range-scan) before any clustering, after `ZORDER BY`, and after Liquid Clustering — same queries, same cluster size, same data volume.
- [ ] TODO: Measure `OPTIMIZE` job duration and cost under each strategy as the table receives its normal upsert load.
- [ ] TODO: Link to the benchmark notebook.

## Consequences

*(TODO)*

## Related

- Builds on ADR-001 (Bronze ingestion feeds this table via Silver).
