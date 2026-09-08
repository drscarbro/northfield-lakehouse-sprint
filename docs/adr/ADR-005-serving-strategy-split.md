# ADR-005: Real-time serving for recommendations, nightly batch for churn scoring

## Status

Planned — due Week 6 (Oct 13–19)

## Date

TBD

## Context

Both models come out of the same MLflow Model Registry, and the reflex is to deploy them the same way. They have different consumers, though: the recommender needs a response inline while a shopper is browsing; churn scores feed a weekly retention-campaign list that doesn't need to be fresher than a day old. Deploying both to a real-time endpoint (or both as batch) would optimize for consistency of operations over fitness to the actual use case.

## Decision Drivers

- Latency requirement of the consumer: storefront page load vs. a nightly marketing job.
- Cost: a real-time serving endpoint runs continuously; a batch job runs for minutes, once a day.
- Staleness tolerance: how old can a prediction be before it's wrong in a way that matters to the business.

## Options Considered

### Option A: Both models on real-time Model Serving

- Pros:
- Cons:

### Option B: Both models as nightly batch scoring jobs

- Pros:
- Cons:

### Option C: Recommender on real-time serving, churn scoring as nightly batch

- Pros:
- Cons:

## Decision

*(TODO)*

## Evidence

- [ ] TODO: p99 latency of the real-time serving endpoint under simulated storefront load.
- [ ] TODO: Cost comparison — real-time endpoint uptime cost vs. batch job runtime cost for churn scoring specifically.
- [ ] TODO: Link to the serving endpoint config and the batch scoring job definition.

## Consequences

*(TODO)*

## Related

- Depends on ADR-004 (feature table design feeds both models).
