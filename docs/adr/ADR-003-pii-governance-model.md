# ADR-003: Column masking via dynamic views over separate PII tables

## Status

Planned — due Week 3 (Sep 22–28)

## Date

TBD

## Context

The Silver `customers` table carries PII (email, address) that analysts need query access to the surrounding table for, but not to the raw values. Two standard patterns solve this: mask the sensitive columns in place with a dynamic view gated on group membership, or physically split PII into a separately-permissioned table joined back in only for privileged roles. This decision determines the grants model for the rest of the pipeline.

## Decision Drivers

- Query ergonomics for analysts: a masked view keeps one table to query; a split table forces a join for anyone who needs the full record.
- Blast radius of a grants misconfiguration: masking failure exposes a column; a split-table join misconfiguration can silently drop rows if done as an inner join.
- Auditability: which approach makes it easier to answer "who could have seen this customer's email on this date" during a review.

## Options Considered

### Option A: Dynamic view with `is_account_group_member()`

- Pros:
- Cons:

### Option B: Separate PII table, joined back in only for privileged roles

- Pros:
- Cons:

## Decision

*(TODO)*

## Evidence

- [ ] TODO: Query the `customers_secure` view as both an `analyst` and a `pii-readers` principal; capture the actual output difference.
- [ ] TODO: Unity Catalog audit log entries showing the grant check firing.
- [ ] TODO: Link to the view DDL.

## Consequences

*(TODO)*

## Related

- Depends on the Unity Catalog three-level namespace and grants model set up earlier in Week 3.
