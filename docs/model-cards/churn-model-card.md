# Model Card: Northfield churn classifier

*Due Week 5 (Oct 6 – 12).*

## Model details

- **Model type**: TODO (e.g., LightGBM classifier)
- **Version**: TODO
- **Owner**: <you>
- **Last updated**: TODO

## Intended use

Feeds a weekly retention-campaign target list. Not intended for real-time decisions at checkout — batch-scored nightly, so a customer's score can be up to 24 hours stale by design (see [ADR-005](../adr/ADR-005-serving-strategy-split.md)).

## Training data

- Source: Feature Engineering in Unity Catalog churn feature table (see [ADR-004](../adr/ADR-004-feature-store-point-in-time-design.md))
- Time window: TODO
- Row count / class balance: TODO
- Known gaps: TODO

## Features

| Feature | Source | Point-in-time key? | Notes |
|---|---|---|---|
| | | | |

## Evaluation

| Metric | Value | Evaluated on |
|---|---|---|
| AUC | TODO | TODO |
| AUC (AutoML baseline) | TODO | TODO |

## Limitations

*(TODO — state plainly once you've evaluated across customer segments.)*

## Monitoring

- Drift signal: input feature distribution on the churn inference table (Lakehouse Monitoring)
- Alert threshold: TODO
- Retraining trigger: TODO

## Links

- Training notebook / job: TODO
- MLflow experiment: TODO
