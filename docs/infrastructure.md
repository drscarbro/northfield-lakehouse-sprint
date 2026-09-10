# Infrastructure reference

The AWS and Databricks resources backing Northfield Commerce, so Week 3's CI/CD and governance work doesn't have to rediscover them. Not a secrets file — no keys or tokens live here, only names and ARNs.

## Databricks workspace

| | |
|---|---|
| Workspace | `https://dbc-5d90d0f0-c1fb.cloud.databricks.com` |
| Metastore | `metastore_aws_us_east_2` (`a3e9ec18-cb35-44c8-9101-24283fbc4dce`), region `us-east-2` |
| CLI profile | `default` (OAuth via `databricks auth login`) |

## Unity Catalog

| | |
|---|---|
| Catalog | `northfield_dev` |
| Schemas | `bronze`, `silver`, `gold` |
| Storage credential | `northfield-uc-credential` → IAM role `northfield-uc-access-role` |
| External location | `northfield-lakehouse-location` → `s3://northfield-lakehouse-811625213267/` |
| Catalog storage root | `s3://northfield-lakehouse-811625213267/northfield_dev` |

See [ADR-000](adr/ADR-000-catalog-schema-layout.md) for why this is one catalog per environment rather than one per medallion layer.

## AWS (account `811625213267`)

| Resource | Name | Purpose |
|---|---|---|
| S3 bucket | `northfield-lakehouse-811625213267` | Backs the Unity Catalog managed storage for `northfield_dev`. Public access fully blocked, default SSE-S3 encryption. |
| IAM role | `northfield-uc-access-role` | Assumed by Databricks' Unity Catalog master role (cross-account, external-ID gated) to read/write the bucket on Unity Catalog's behalf. |
| IAM user | `northfield-lakehouse-provisioner` | Scoped to managing this one bucket and IAM resources prefixed `northfield-*` — used for all infra provisioning instead of the AWS root user. |
| AWS CLI profile | `northfield` | Points at the provisioner user's credentials. |

## Provisioning a new environment (staging / prod)

Repeat the pattern from ADR-000 with a new suffix:

1. New S3 bucket: `northfield-lakehouse-<account-id>-<env>`.
2. New IAM role `northfield-uc-access-role-<env>` with the same trust-policy shape (placeholder external ID → create storage credential → update trust policy with the real one).
3. New storage credential + external location + catalog (`northfield_<env>`), same three schemas inside.

## Known trade-offs, not yet addressed

- The storage credential and external location are `isolation_mode: OPEN` — usable by anything with catalog-level permission, not scoped to specific catalogs/tables. Fine for a single-developer dev environment; revisit before treating `staging`/`prod` the same way.
