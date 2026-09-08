# Building the Northfield Commerce Lakehouse — Part 1: Ingestion to Governed Gold

*Due Week 4 (Sep 29 – Oct 5). Draws on ADR-001, ADR-002, ADR-003.*

## Summary

*(TODO — 3-4 sentences once the build is done. What the pipeline does, the hardest decision, the headline result.)*

## The problem

Northfield Commerce has three source systems with genuinely different freshness, volume, and schema-stability characteristics, and a requirement to serve both BI and, eventually, ML from one governed Gold layer without duplicating logic.

## System overview

*(Embed the north-star diagram, or the subset of it this part covers: Sources → Bronze → Silver → Gold → BI.)*

## The decisions

### Matching ingestion pattern to source shape ([ADR-001](../adr/ADR-001-ingestion-pattern-per-source.md))

*(TODO)*

### Liquid Clustering vs. Z-Order on the orders fact ([ADR-002](../adr/ADR-002-clustering-strategy-orders-fact.md))

*(TODO)*

### PII governance via dynamic views ([ADR-003](../adr/ADR-003-pii-governance-model.md))

*(TODO)*

## Results

| Metric | Before | After |
|---|---|---|
| Orders fact point-lookup p95 | | |
| Orders fact range-scan p95 | | |
| Bronze ingestion latency (clickstream) | | |
| Job cluster cost/day | | |

## What I'd do differently

*(TODO)*

## Links

- Repo: <link>
- ADR-001, ADR-002, ADR-003
- Diagram: `diagrams/`
