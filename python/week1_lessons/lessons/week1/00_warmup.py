"""WARM-UP - lists, dicts, sets (things you already know). ~15 min, no files yet.

Fill in each function, then run:
    uv run python lessons/week1/00_warmup.py
Each exercise prints PASS or FAIL.
"""

# Five payments, written by hand (later they'll come from a CSV)
payments = [
    {"payment_id": 1, "customer_id": 1, "amount": 2.99},
    {"payment_id": 2, "customer_id": 1, "amount": 0.99},
    {"payment_id": 3, "customer_id": 2, "amount": 5.99},
    {"payment_id": 4, "customer_id": 3, "amount": 4.99},
    {"payment_id": 5, "customer_id": 2, "amount": 9.99},
]


def total_for_customer(rows, customer_id):
    """W1: total amount paid by one customer. Use a for-loop and an if."""
    total = 0
    for row in rows:
        if customer_id in row.values():
            total += row["amount"]

    return total


def distinct_customers(rows):
    """W2: the SET of customer_ids that appear in rows."""
    customer_set = set()
    for row in rows:
        if row["customer_id"] not in customer_set:
            customer_set.add(row["customer_id"])
        
    return customer_set


def payments_per_customer(rows):
    """W3: a DICT {customer_id: number_of_payments}. Use a loop and dict.get()."""
    payments_per_customer= {}
    for row in rows:
        customer_id = row["customer_id"]
        payments_per_customer.get("customer_id", customer_id)

    print(payments_per_customer)
    return payments_per_customer


# ---------------- self-check (don't edit below) ----------------
def check(name, got, expected):
    if isinstance(expected, float) and isinstance(got, float):
        ok = round(got, 2) == expected
    else:
        ok = got == expected
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + ("" if ok else f"  got {got!r}, expected {expected!r}"))


check("W1 total_for_customer", total_for_customer(payments, 1), 3.98)
check("W2 distinct_customers", distinct_customers(payments), {1, 2, 3})
check("W3 payments_per_customer", payments_per_customer(payments), {1: 2, 2: 2, 3: 1})
