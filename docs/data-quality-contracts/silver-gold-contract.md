# Data Quality Contract: Silver → Gold (orders, customers)

*Due Week 2 (Sep 15 – 21), as part of the DLT pipeline rebuild.*

| Field | Rule | Action on failure | Rationale |
|---|---|---|---|
| `order_id` | NOT NULL, unique | `expect_or_fail` | TODO |
| `customer_id` | NOT NULL, exists in customer dimension | `expect_or_drop` | TODO |
| `order_timestamp` | not in the future | `expect_or_drop` | TODO |
| `email` | matches email format | `expect` (log only) | TODO |
| | | | |

## Actions, defined

- **`expect_or_fail`**: halts the pipeline.
- **`expect_or_drop`**: drops the offending row, pipeline continues.
- **`expect` (log only)**: records the violation without changing pipeline behavior.

## Review

*(TODO — revisit after the first real schema change from an upstream source.)*
