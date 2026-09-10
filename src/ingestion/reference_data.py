"""Static reference sets shared by all three source simulators.

Keeping customer/product/warehouse IDs consistent across clickstream, orders,
and inventory is what makes the simulated data joinable in Silver/Gold later —
three simulators generating unrelated random IDs would produce a Bronze layer
that no join in Week 2 could actually use.
"""

import random

CUSTOMER_IDS = [f"CUST-{i:05d}" for i in range(1, 501)]

PRODUCT_CATALOG = [
    {"product_id": f"SKU-{i:05d}", "category": category, "price": price}
    for i, (category, price) in enumerate(
        [
            ("outdoor", 89.99), ("outdoor", 45.00), ("kitchen", 24.50),
            ("kitchen", 129.00), ("electronics", 199.99), ("electronics", 39.99),
            ("apparel", 59.00), ("apparel", 18.00), ("home", 74.25),
            ("home", 12.99), ("outdoor", 220.00), ("electronics", 899.00),
        ]
        * 20,
        start=1,
    )
]

WAREHOUSES = ["WH-EAST", "WH-CENTRAL", "WH-WEST"]

EVENT_TYPES_WEIGHTED = (
    ["view"] * 70 + ["add_to_cart"] * 20 + ["purchase"] * 7 + ["remove_from_cart"] * 3
)


def random_customer() -> str:
    return random.choice(CUSTOMER_IDS)


def random_product() -> dict:
    return random.choice(PRODUCT_CATALOG)


def random_warehouse() -> str:
    return random.choice(WAREHOUSES)
