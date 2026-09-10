"""Simulates the clickstream source feed: many small JSON files landing
continuously, the shape Auto Loader's incremental file listing is built for.

Run from the repo root to produce one batch of files:

    python -m src.ingestion.clickstream_source --batches 5 --events-per-batch 200

Each call appends new files under data/raw/clickstream/ — it never rewrites
existing ones, so re-running mimics a real stream arriving over time rather
than a single bulk load.
"""

import argparse
import json
import random
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .reference_data import EVENT_TYPES_WEIGHTED, random_customer, random_product

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "clickstream"


def generate_event(session_id: str) -> dict:
    product = random_product()
    return {
        "event_id": str(uuid.uuid4()),
        "session_id": session_id,
        "customer_id": random_customer(),
        "event_type": random.choice(EVENT_TYPES_WEIGHTED),
        "product_id": product["product_id"],
        "event_timestamp": datetime.now(timezone.utc).isoformat(),
    }


def write_batch(events_per_batch: int) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    session_id = str(uuid.uuid4())
    events = [generate_event(session_id) for _ in range(events_per_batch)]

    filename = f"clickstream_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')}.json"
    path = OUTPUT_DIR / filename
    with path.open("w") as f:
        for event in events:
            f.write(json.dumps(event) + "\n")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batches", type=int, default=1, help="number of files to write")
    parser.add_argument("--events-per-batch", type=int, default=100)
    parser.add_argument(
        "--interval-seconds", type=float, default=0.0,
        help="pause between files, to simulate real arrival pacing",
    )
    args = parser.parse_args()

    for i in range(args.batches):
        path = write_batch(args.events_per_batch)
        print(f"wrote {args.events_per_batch} events -> {path}")
        if args.interval_seconds and i < args.batches - 1:
            time.sleep(args.interval_seconds)


if __name__ == "__main__":
    main()
