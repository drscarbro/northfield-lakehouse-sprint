# Model Card: <model name>

## Model details

- **Model type**: (e.g., gradient-boosted classifier)
- **Version**: (Model Registry version/alias)
- **Owner**: <you>
- **Last updated**: YYYY-MM-DD

## Intended use

What decision does this model's output feed? Who consumes the prediction, and what do they do with it? State what the model is *not* intended for as clearly as what it is.

## Training data

- Source tables (Feature Store tables, with links)
- Time window covered
- Row count, class balance (for classifiers)
- Known gaps or biases in the training population

## Features

| Feature | Source | Point-in-time key? | Notes |
|---|---|---|---|
| | | | |

## Evaluation

| Metric | Value | Evaluated on |
|---|---|---|
| | | |

Include the baseline you're beating (AutoML run, previous model version, or a naive heuristic) — a metric with no comparison point is not evidence of anything.

## Limitations

Stated plainly, not hedged. What inputs or populations does this model perform worse on? What would make you not trust its output?

## Monitoring

- Drift signal being watched (e.g., input feature distribution)
- Alert threshold
- Retraining trigger

## Links

- Training notebook / job
- MLflow experiment
- Feature table definitions
