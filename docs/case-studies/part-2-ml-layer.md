# Building the Northfield Commerce Lakehouse — Part 2: Features to Production Models

*Due Week 6 (Oct 13 – 19). Draws on ADR-004, ADR-005. Reads as a continuation of Part 1, not a standalone piece.*

## Summary

*(TODO)*

## The problem

Two models with genuinely different consumers — a recommender feeding a live storefront, a churn classifier feeding a weekly retention job — coming out of the same feature layer and the same registry. The naive move is to treat them identically.

## System overview

*(Embed the full north-star diagram, now with the ML branch fully built: Gold → Feature Store → MLflow Training → Model Registry → Real-time Serving / Batch Scoring.)*

## The decisions

### Point-in-time correctness on the churn feature table ([ADR-004](../adr/ADR-004-feature-store-point-in-time-design.md))

*(TODO)*

### Splitting the deployment path by consumer, not by default ([ADR-005](../adr/ADR-005-serving-strategy-split.md))

*(TODO)*

## Results

| Metric | Before | After |
|---|---|---|
| Churn model AUC (leaking vs. point-in-time features) | | |
| Recommender endpoint p99 latency | | |
| Batch scoring job runtime/cost | | |

## What I'd do differently

*(TODO)*

## Links

- Repo: <link>
- ADR-004, ADR-005
- Part 1: [part-1-lakehouse-build.md](./part-1-lakehouse-build.md)
