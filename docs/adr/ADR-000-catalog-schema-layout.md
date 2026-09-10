# ADR-000: One catalog per environment, schemas for the medallion layers

## Status

Accepted

## Date

2026-09-10

## Context

Unity Catalog's three-level namespace (`catalog.schema.table`) gives two natural ways to model Northfield Commerce: a catalog per medallion layer (`bronze`, `silver`, `gold` as catalogs, each with per-domain schemas inside), or a catalog per environment (`northfield_dev`/`staging`/`prod`) with the medallion layers as schemas inside each. This has to be decided before any table gets created, since moving a table between catalogs later is a real migration, not a rename.

## Decision Drivers

- Databricks Asset Bundles (Week 3) deploy the same pipeline definitions across dev/staging/prod by swapping a target — that pattern wants the environment to be the top-level boundary, not the layer.
- Unity Catalog grants are most naturally scoped at the catalog level for broad strokes ("analysts can read this whole environment's Gold data") and at the schema level for finer control — catalog-per-layer would force environment distinctions down into schema-naming conventions instead (`bronze_dev`, `bronze_prod`), which is exactly the kind of naming-as-structure smell Unity Catalog's namespace exists to avoid.
- A single managed storage location (bucket) backs a catalog's storage root by default — one bucket per environment is a cleaner blast radius than one bucket per layer.

## Options Considered

### Option A: Catalog per medallion layer (`bronze`, `silver`, `gold`)

- Pros: the medallion layer is immediately visible in every table's fully-qualified name.
- Cons: environment (dev/staging/prod) has nowhere to live except in schema or table naming conventions; cross-environment promotion via DAB targets fights the namespace instead of matching it.

### Option B: Catalog per environment (`northfield_dev`, `northfield_staging`, `northfield_prod`), schemas for `bronze`/`silver`/`gold`

- Pros: matches the DAB deployment model directly — a target environment is a catalog, full stop; grants scope naturally ("engineers get northfield_dev, analysts get northfield_prod.gold only").
- Cons: the medallion layer is one level deeper in the namespace (`northfield_prod.gold.orders` vs. a hypothetical `gold.prod_orders`) — a minor readability cost, not a functional one.

## Decision

Option B. One catalog per environment, with `bronze`, `silver`, and `gold` as schemas inside it. `northfield_dev` is live today; `northfield_staging` and `northfield_prod` get created the same way once Week 3's DAB targets need them.

## Evidence

- Storage credential (`northfield-uc-credential`) validated clean against the backing S3 bucket — READ, LIST, WRITE, DELETE, and PATH_EXISTS all passed via `databricks storage-credentials validate`.
- Catalog and all three schemas created and confirmed via `databricks catalogs list` / `databricks schemas list northfield_dev`.
- Operational note, not just theory: the IAM trust policy update (adding the real external ID) took roughly 20-30 seconds to propagate before validation started passing — worth remembering before assuming a misconfiguration on the next credential.

## Consequences

### Positive

- Environment promotion (dev → staging → prod) is a catalog swap in the DAB target config, not a schema-renaming exercise.
- Grants model from ADR-003 has an obvious place to attach: catalog-level for environment access, schema-level for layer access.

### Negative / trade-offs accepted

- One more namespace level between a query and the table it wants (`catalog.schema.table` where schema always equals a medallion layer) — acceptable, since every query in this project already has to specify the environment anyway.

### Follow-ups

- Create `northfield_staging` and `northfield_prod` catalogs (same bucket-per-environment pattern, new IAM role + storage credential each) when Week 3's CI/CD work needs real target environments.

## Related

- Precedes ADR-001 (ingestion pattern) — Bronze tables from Week 1 land in `northfield_dev.bronze`.
- Feeds directly into ADR-003 (PII governance model), which grants against this same catalog/schema structure.
