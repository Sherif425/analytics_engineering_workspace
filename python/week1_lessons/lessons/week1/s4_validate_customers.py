"""SOLO 4 - validate customer.csv with logging (uses: g1-g5, everything together).

Goal: check every customer row, log each problem, never crash.

Step 0 - LOOK AT THE DATA FIRST (always, before writing rules)
  In a Python shell, print the distinct values of "active":
      {row["active"] for row in read_csv(DATA_DIR / "customer.csv")}
  Your export might say {"0", "1"} or {"false", "true"}. Write what you found in
  ALLOWED_ACTIVE below. The rules come from the data, not from a guess.

Tasks
  1. Set up logging with the g5 recipe: screen + file logs/s4_customers.log.
  2. Implement check_customer(row, valid_store_ids, allowed_active) -> list[str]
     Rules (one message per broken rule):
       a. customer_id is a whole number             (int(...) inside try/except ValueError)
       b. email contains "@"
       c. active is one of allowed_active
       d. store_id exists in valid_store_ids        (ids from store.csv)
  3. Implement validate_file(path) -> int  (returns the number of bad rows)
       - if the file doesn't exist: log.error and return -1
       - log.info how many rows were read
       - for every row: run check_customer, ALSO check customer_id is unique
         (a set of seen ids, like g4), and log.warning each problem as
         "customer.csv line 17: email 'x' has no @"
       - log.info a summary: "599 rows, 599 valid, 0 invalid"

Run:  uv run python lessons/week1/s4_validate_customers.py
Then: cat logs/s4_customers.log
"""

import csv
import logging
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "sakila_csv"

ALLOWED_ACTIVE: set[str] = set()  # TODO after Step 0

# TODO: logging recipe here
log = logging.getLogger(__name__)


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read a CSV file into a list of dicts (one dict per row)."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check_customer(row: dict[str, str], valid_store_ids: set[str], allowed_active: set[str]) -> list[str]:
    # TODO
    return []


def validate_file(path: Path) -> int:
    # TODO
    return None


# ---------------- self-check (don't edit below) ----------------
if __name__ == "__main__":
    good = {"customer_id": "1", "email": "A@B.org", "active": "1", "store_id": "1"}
    cases = [
        ("valid row", good, 0),
        ("customer_id 'abc'", {**good, "customer_id": "abc"}, 1),
        ("email without @", {**good, "email": "mary.smith"}, 1),
        ("active '9'", {**good, "active": "9"}, 1),
        ("store_id '7'", {**good, "store_id": "7"}, 1),
        ("everything wrong", {"customer_id": "", "email": "", "active": "", "store_id": ""}, 4),
    ]
    for name, row, n in cases:
        got = check_customer(row, {"1", "2"}, {"0", "1"})
        ok = len(got) == n
        print(f"{'PASS' if ok else 'FAIL'}  check_customer: {name:<18} -> {got}")

    print("\nReal file:")
    bad = validate_file(DATA_DIR / "customer.csv")
    print("PASS  real customer.csv has 0 bad rows" if bad == 0 else f"FAIL  got {bad} bad rows, expected 0")
    print("PASS  missing file returns -1" if validate_file(DATA_DIR / "nope.csv") == -1 else "FAIL  missing file")
    print("PASS  log file written" if (PROJECT_ROOT / "logs" / "s4_customers.log").exists() else "FAIL  no log file")
