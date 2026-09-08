# ADR-004: Point-in-time keys on the churn feature table

## Status

Planned — due Week 5 (Oct 6–12)

## Date

TBD

## Context

The churn feature table is built from the same Gold layer used for BI, which means it's easy to accidentally join in information that wouldn't have been available at the time a historical training label was generated — classic label leakage. The Feature Engineering client in Unity Catalog supports point-in-time lookups via a timestamp key, but only if the feature table is designed for it from the start.

## Decision Drivers

- Training/serving skew: features computed for training must be reproducible at serving time from the same logic.
- Leakage risk: any feature that uses information from after the label's cutoff date inflates offline metrics and fails in production.
- Join cost: point-in-time joins are more expensive than a plain key join — worth confirming the cost is acceptable at Northfield's data volume.

## Options Considered

### Option A: Primary key only (customer_id), latest value always joined

- Pros:
- Cons:

### Option B: Composite key (customer_id + timestamp key), point-in-time join at training time

- Pros:
- Cons:

## Decision

*(TODO)*

## Evidence

- [ ] TODO: Deliberately construct one leaking feature and one point-in-time-correct feature; show the offline metric gap between them on the same model.
- [ ] TODO: Link to the feature table definition and the training notebook's `create_training_set` call.

## Consequences

*(TODO)*

## Related

- Builds on the Gold-layer star schema from ADR-002.
