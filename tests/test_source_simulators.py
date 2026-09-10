"""Smoke tests for the three source simulators.

These check shape and referential consistency (every generated customer_id
and product_id is one Silver's dimension tables will actually recognize) —
not full unit coverage, just enough to catch a broken simulator before it
quietly corrupts Bronze.
"""

import csv
import json

from src.ingestion import clickstream_source, inventory_source, orders_source
from src.ingestion.reference_data import CUSTOMER_IDS, PRODUCT_CATALOG, WAREHOUSES

KNOWN_PRODUCT_IDS = {p["product_id"] for p in PRODUCT_CATALOG}


def test_clickstream_batch_shape(tmp_path, monkeypatch):
    monkeypatch.setattr(clickstream_source, "OUTPUT_DIR", tmp_path)
    path = clickstream_source.write_batch(events_per_batch=20)

    lines = path.read_text().strip().splitlines()
    assert len(lines) == 20

    for line in lines:
        event = json.loads(line)
        assert event["customer_id"] in CUSTOMER_IDS
        assert event["product_id"] in KNOWN_PRODUCT_IDS
        assert event["event_type"] in {"view", "add_to_cart", "purchase", "remove_from_cart"}


def test_orders_batch_has_inserts_and_updates(tmp_path, monkeypatch):
    monkeypatch.setattr(orders_source, "OUTPUT_DIR", tmp_path)
    orders_source._KNOWN_ORDERS.clear()

    # first batch is all inserts (no existing orders to update yet)
    orders_source.write_batch(orders_per_batch=10)
    # second batch, against warmed-up state, should include at least one update
    path = orders_source.write_batch(orders_per_batch=30)

    records = [json.loads(line) for line in path.read_text().strip().splitlines()]
    ops = {r["op"] for r in records}
    assert "insert" in ops
    assert "update" in ops

    for record in records:
        if record["op"] == "insert":
            assert record["customer_id"] in CUSTOMER_IDS
            assert record["product_id"] in KNOWN_PRODUCT_IDS
        else:
            assert record["status"] in {"fulfilled", "cancelled", "refunded"}


def test_inventory_snapshot_covers_every_warehouse(tmp_path, monkeypatch):
    monkeypatch.setattr(inventory_source, "OUTPUT_DIR", tmp_path)
    paths = inventory_source.write_snapshot(inventory_source.date.today())

    assert {p.stem for p in paths} == set(WAREHOUSES)

    with paths[0].open() as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == len(PRODUCT_CATALOG)
    assert all(int(row["quantity_on_hand"]) >= 0 for row in rows)
