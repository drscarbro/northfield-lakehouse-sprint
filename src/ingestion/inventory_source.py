"""Simulates the inventory source feed: one full snapshot file per warehouse,
per day — the shape that justifies a scheduled batch read instead of Auto
Loader in ADR-001 (there's no "incremental" here, every run is a full
replace of that day's state).

Run from the repo root to produce today's snapshot for every warehouse:

    python -m src.ingestion.inventory_source
    python -m src.ingestion.inventory_source --date 2026-09-11
"""

import argparse
import csv
import random
from datetime import date
from pathlib import Path

from .reference_data import PRODUCT_CATALOG, WAREHOUSES

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "inventory"


def write_snapshot(snapshot_date: date) -> list[Path]:
    written = []
    for warehouse in WAREHOUSES:
        day_dir = OUTPUT_DIR / f"dt={snapshot_date.isoformat()}"
        day_dir.mkdir(parents=True, exist_ok=True)
        path = day_dir / f"{warehouse}.csv"

        with path.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["warehouse", "product_id", "quantity_on_hand", "snapshot_date"])
            for product in PRODUCT_CATALOG:
                writer.writerow(
                    [warehouse, product["product_id"], random.randint(0, 500), snapshot_date.isoformat()]
                )
        written.append(path)
    return written


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", type=str, default=None, help="YYYY-MM-DD, defaults to today")
    args = parser.parse_args()

    snapshot_date = date.fromisoformat(args.date) if args.date else date.today()
    for path in write_snapshot(snapshot_date):
        print(f"wrote snapshot -> {path}")


if __name__ == "__main__":
    main()
