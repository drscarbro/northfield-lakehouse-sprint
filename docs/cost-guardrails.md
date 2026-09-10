# Cost guardrails

This is a personal AWS account paying real money for a learning project — the guardrails here exist because "I'll remember to turn it off" is not a control, and because cost/monitoring is itself a Data Engineer Professional exam domain (Week 3). Treat this doc as load-bearing, not aspirational.

## AWS Budget

- **Threshold**: $100/month, alerts at 50% / 80% (actual spend) and 100% (forecasted)
- **Alert email**: drscarbro@gmail.com
- Set up manually in AWS Console (Billing and Cost Management → Budgets) rather than via CLI — the scoped `northfield` IAM user deliberately doesn't have `budgets:*` permission, and extending it just for a one-time setup wasn't worth widening that user's blast radius.
- This is the real backstop. Everything else below reduces the odds of tripping it; the budget alert is what catches it if they fail.

## Databricks cluster policy

`northfield-cost-guardrail` (policy ID `001979F4AEC7CF3E`) — use this policy ID for every cluster this project creates, including the ones defined inside Databricks Asset Bundle resources from Week 3 onward:

| Setting | Constraint |
|---|---|
| Auto-termination | 5–45 min, defaults to 20 |
| Node type (worker + driver) | `i3.xlarge` or `m5.large` only |
| Worker count | 0–2 |
| Availability | Spot with on-demand fallback |

This is a soft guardrail, not a hard one — as the workspace's only admin, nothing stops an unrestricted cluster from being created outside this policy. The discipline is: always attach it anyway.

## Pre-flight / post-flight check

Run before ending any work session:

```
./scripts/check_running_compute.sh
```

Checks clusters, SQL warehouses, active job runs, and any custom (non-foundation-model) serving endpoints. Exits non-zero if anything is still running that shouldn't be.

## Known future cost risks, by week

- **Week 4 (streaming)**: the sessionized clickstream aggregation uses a continuous trigger by design (that's the point of the exercise) — don't leave it running between sessions. Use `.trigger(availableNow=True)` for everyday development and only switch to continuous mode for the specific benchmark/demo that needs it.
- **Week 6 (real-time serving)**: a Model Serving endpoint for the recommender has standing compute cost the moment it's deployed, unlike the pay-per-token foundation model endpoints already in this workspace. Delete it after capturing the latency numbers ADR-005 needs, redeploy when it's time to re-demo.

## Trial period note

The Databricks free trial covers DBUs for 14 days; the underlying AWS EC2/S3/data-transfer costs are billed by AWS regardless and are what the budget above is actually watching. After the trial window, confirm whether the workspace converts to pay-as-you-go DBU billing before starting a new week's build.
