#!/usr/bin/env bash
# Pre-flight / post-flight cost check: anything left running after a session
# is the single most common way a personal Databricks project runs up an
# AWS bill. Run this before you close your laptop.
#
# Requires: databricks CLI (authenticated), jq

set -euo pipefail

WARN=0

echo "=== Clusters ==="
clusters=$(databricks clusters list -o json)
running=$(echo "$clusters" | jq -r '.[] | select(.state != "TERMINATED") | "\(.cluster_name)  [\(.state)]"')
if [ -n "$running" ]; then
  echo "$running"
  WARN=1
else
  echo "none running."
fi

echo ""
echo "=== SQL Warehouses ==="
warehouses=$(databricks warehouses list -o json)
running=$(echo "$warehouses" | jq -r '.[] | select(.state != "STOPPED") | "\(.name)  [\(.state)]"')
if [ -n "$running" ]; then
  echo "$running"
  WARN=1
else
  echo "none running."
fi

echo ""
echo "=== Jobs currently executing ==="
active_runs=$(databricks jobs list -o json | jq -r '.[].job_id' | while read -r job_id; do
  databricks jobs list-runs --job-id "$job_id" --active-only true -o json 2>/dev/null || true
done | jq -s 'add // []')
count=$(echo "$active_runs" | jq 'length')
if [ "$count" -gt 0 ]; then
  echo "$active_runs" | jq -r '.[] | "\(.run_name // .job_id)  [\(.state.life_cycle_state)]"'
  WARN=1
else
  echo "none running."
fi

echo ""
echo "=== Model Serving endpoints (non-foundation-model only) ==="
# Foundation model (system.ai.*) endpoints are pay-per-token with no idle
# cost -- only custom endpoints (ours) carry standing compute cost.
custom_endpoints=$(databricks serving-endpoints list -o json | jq -r '.[] | select(.config.served_entities[0].entity_name // "" | startswith("system.ai.") | not) | .name')
if [ -n "$custom_endpoints" ]; then
  echo "$custom_endpoints"
  WARN=1
else
  echo "none deployed."
fi

echo ""
if [ "$WARN" -eq 1 ]; then
  echo "WARNING: compute is still running. Confirm it's intentional before you stop working."
  exit 1
else
  echo "Clean. Nothing billing right now beyond storage."
fi
