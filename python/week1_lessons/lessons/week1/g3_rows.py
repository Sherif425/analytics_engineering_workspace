"""GUIDED 3 - Answering questions with lists, dicts, sets (self-tests 1-3).

CONCEPT
-------
After read_csv() you have a LIST OF DICTS: the whole table in memory.
To answer a question, pick the data structure that matches the question:

  Question shape                         Structure          SQL equivalent
  -------------------------------------  -----------------  ----------------
  "keep only rows where ..."             list + if          WHERE
  "how many per X?"                      Counter / dict     GROUP BY + COUNT
  "which distinct values?"               set                DISTINCT
  "which keys are in A but not in B?"    set - set          EXCEPT / anti-join
  "look up a value by its id"            dict {id: value}   JOIN on a key

Run:   uv run python lessons/week1/g3_rows.py
"""

import csv
from collections import Counter
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "sakila_csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read a CSV file into a list of dicts (one dict per row)."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# --- Self-test 1: load rental.csv into a list of dicts -----------------------
rentals = read_csv(DATA_DIR / "rental.csv")
customers = read_csv(DATA_DIR / "customer.csv")
print(f"1) Loaded {len(rentals)} rentals and {len(customers)} customers")

# --- Self-test 2: top 5 customers by number of rentals -----------------------
# Step A: the plain-loop way (so you see what Counter does for you)
counts: dict[str, int] = {}
for row in rentals:
    cid = row["customer_id"]
    counts[cid] = counts.get(cid, 0) + 1  # .get(key, 0): 0 if not seen yet
print("\n2a) Rentals for customer 148 (plain dict):", counts["148"])

# Step B: Counter does exactly that loop in one line, and can sort
rental_counts = Counter(row["customer_id"] for row in rentals)
print("2b) Top 5 customers by rentals (Counter):")
for cid, n in rental_counts.most_common(5):
    print(f"    customer {cid:>3}: {n} rentals")

# Step C: make it readable with a lookup dict {customer_id: full name}  (= JOIN)
name_by_id = {c["customer_id"]: f"{c['first_name']} {c['last_name']}" for c in customers}
print("2c) Same top 5 with names (dict lookup = JOIN):")
for cid, n in rental_counts.most_common(5):
    print(f"    {name_by_id[cid]:<22} {n} rentals")

# --- Self-test 3: customer_ids in rental that are missing from customer --------
rental_customer_ids = {row["customer_id"] for row in rentals}  # set = DISTINCT
known_customer_ids = {c["customer_id"] for c in customers}
orphans = rental_customer_ids - known_customer_ids  # set difference = EXCEPT
print("\n3) Distinct customers in rental:", len(rental_customer_ids))
print("   Orphan customer_ids (in rental, not in customer):", orphans or "none")

# Why a set and not a list for this?  "x in a_set" is instant;
# "x in a_list" checks every element. With 16,044 rows that difference is real.

# TRY THIS
# a) Top 3 inventory_ids by number of rentals.
# b) Which customers have NEVER rented anything?  (known_customer_ids - rental_customer_ids)
# c) Count rentals per staff_id with Counter. Compare with SQL:
#    SELECT staff_id, COUNT(*) FROM rental GROUP BY staff_id;
