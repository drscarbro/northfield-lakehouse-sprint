# Northfield Lakehouse Sprint

[![6-Week Plan](https://img.shields.io/badge/6--week%20plan-view%20artifact-1F7A6C?style=flat-square)](https://claude.ai/code/artifact/b2a03db2-2821-4192-ac0c-749113537d40)

A Lakehouse + ML system built over six weeks while preparing for the Databricks Certified Data Engineer Professional and Machine Learning Professional exams. The full week-by-week plan lives in [this artifact](https://claude.ai/code/artifact/b2a03db2-2821-4192-ac0c-749113537d40); this repo is where the plan turns into evidence.

Northfield Commerce is a fictional retailer. The three source feeds (clickstream, orders, inventory), the medallion pipeline, and the two downstream models are the reference system every decision below is made about.

## Decision log

| ADR | Decision | Status | Week |
|---|---|---|---|
| [ADR-000](docs/adr/ADR-000-catalog-schema-layout.md) | One catalog per environment, schemas for the medallion layers | Accepted | 1 |
| [ADR-001](docs/adr/ADR-001-ingestion-pattern-per-source.md) | Auto Loader for clickstream/orders, batch for inventory | Proposed | 1 |
| [ADR-002](docs/adr/ADR-002-clustering-strategy-orders-fact.md) | Liquid Clustering vs. Z-Order on the orders fact | Planned | 2 |
| [ADR-003](docs/adr/ADR-003-pii-governance-model.md) | Column masking via dynamic views | Planned | 3 |
| [ADR-004](docs/adr/ADR-004-feature-store-point-in-time-design.md) | Point-in-time keys on the churn feature table | Planned | 5 |
| [ADR-005](docs/adr/ADR-005-serving-strategy-split.md) | Real-time vs. batch serving split | Planned | 6 |

Status moves `Planned → Proposed → Accepted` as each decision gets made and backed with evidence. Never skip straight to `Accepted` without the Evidence section filled in — an ADR without evidence is a guess with a template around it.

## Status

Week 1 — workspace is live (AWS-backed Databricks trial), Unity Catalog metastore, `northfield_dev` catalog, and `bronze`/`silver`/`gold` schemas are provisioned. Source simulators are built and tested. Next: Auto Loader ingestion into Bronze.

## Structure

```
src/ingestion/             the three source simulators (clickstream, orders CDC, inventory)
tests/                     pytest suite for the simulators
scripts/                   operational scripts (cost check, etc.)
data/raw/                  simulator output, gitignored — regenerate anytime
docs/
  infrastructure.md        AWS + Databricks resource reference (names, ARNs, no secrets)
  cost-guardrails.md        budget threshold, cluster policy, pre-flight cost check
  adr/                     one file per architectural decision, plus template.md
  case-studies/            the two-part portfolio narrative, plus template.md
  model-cards/             one per model, plus template.md
  data-quality-contracts/  one per pipeline stage, plus template.md
diagrams/                  exported architecture diagrams, one per week's system state
```

## Cost guardrails

This is a personal AWS account with a $100/month budget alert on it — see [docs/cost-guardrails.md](docs/cost-guardrails.md) for the threshold, the Databricks cluster policy every cluster in this project should use, and the known cost risks by week. Run this before ending any session:

```
./scripts/check_running_compute.sh
```

## Local dev

```
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt

# generate a batch of raw source data
.venv/bin/python -m src.ingestion.clickstream_source --batches 5 --events-per-batch 200
.venv/bin/python -m src.ingestion.orders_source --batches 5 --orders-per-batch 50
.venv/bin/python -m src.ingestion.inventory_source

# run the test suite
.venv/bin/pytest
```

`data/raw/` uploads to a Unity Catalog volume under `northfield_dev`, and Auto Loader watches that path from there — the simulators themselves don't change.

Every `docs/*/template.md` is reusable beyond this project — copy it for the next decision, the next model, the next pipeline.

## Case studies

- [Part 1: Ingestion to Governed Gold](docs/case-studies/part-1-lakehouse-build.md) — due Week 4
- [Part 2: Features to Production Models](docs/case-studies/part-2-ml-layer.md) — due Week 6

## Workflow

1. Before writing code for a decision point, open the relevant ADR stub and fill in Context and Decision Drivers — you often clarify the real trade-off just by writing this down.
2. Build, then come back and fill in Options Considered and Evidence with what you actually measured.
3. Move Status to `Accepted` once Evidence is real.
4. At the end of Week 4 and Week 6, pull the accepted ADRs into the corresponding case study — don't restate them, distill them.
5. Before closing the laptop: `./scripts/check_running_compute.sh`. Nothing should be running.
