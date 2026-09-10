"""Simulates the orders source feed as a CDC-style stream: each record is an
insert or update against an order, carrying an explicit `op` so downstream
Silver logic has to actually handle upserts (this is what makes ADR-001's
"CDC feed" framing real instead of just append-only events with a different
name).

Run from the repo root to produce one batch of files:

    python -m src.ingestion.orders_source --batches 5 --orders-per-batch 50
"""

import argparse
import json
import random
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .reference_data import random_customer, random_product

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "orders"

# order_id -> current status, so "updates" are believable transitions
# (created -> fulfilled/cancelled/refunded) rather than random noise.
_KNOWN_ORDERS: dict[str, str] = {}


def _new_order() -> dict:
    order_id = f"ORD-{uuid.uuid4().hex[:10]}"
    product = random_product()
    status = "created"
    _KNOWN_ORDERS[order_id] = status
    return {
        "order_id": order_id,
        "customer_id": random_customer(),
        "product_id": product["product_id"],
        "amount": product["price"],
        "status": status,
        "op": "insert",
        "order_timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _update_order() -> dict | None:
    if not _KNOWN_ORDERS:
        return None
    order_id, current_status = random.choice(list(_KNOWN_ORDERS.items()))
    if current_status != "created":
        return None  # terminal states don't get further updates
    new_status = random.choice(["fulfilled", "cancelled", "refunded"])
    _KNOWN_ORDERS[order_id] = new_status
    return {
        "order_id": order_id,
        "status": new_status,
        "op": "update",
        "order_timestamp": datetime.now(timezone.utc).isoformat(),
    }


def generate_batch(orders_per_batch: int) -> list[dict]:
    records = []
    for _ in range(orders_per_batch):
        # ~65% new orders, ~35% status updates to existing ones
        if random.random() < 0.65 or not _KNOWN_ORDERS:
            records.append(_new_order())
        else:
            record = _update_order()
            if record:
                records.append(record)
    return records


def write_batch(orders_per_batch: int) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    records = generate_batch(orders_per_batch)

    filename = f"orders_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')}.json"
    path = OUTPUT_DIR / filename
    with path.open("w") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batches", type=int, default=1)
    parser.add_argument("--orders-per-batch", type=int, default=50)
    parser.add_argument("--interval-seconds", type=float, default=0.0)
    args = parser.parse_args()

    for i in range(args.batches):
        path = write_batch(args.orders_per_batch)
        print(f"wrote batch -> {path}")
        if args.interval_seconds and i < args.batches - 1:
            time.sleep(args.interval_seconds)


if __name__ == "__main__":
    main()
