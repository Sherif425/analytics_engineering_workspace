"""SOLO 2 - tuple keys and grouping (self-test 4; uses: g2, g3, g4).

Goal: total amount paid per (customer_id, month), then the 3 biggest.

SQL you'd write:
    SELECT customer_id, strftime(payment_date, '%Y-%m') AS month, SUM(amount)
    FROM payment GROUP BY 1, 2 ORDER BY 3 DESC LIMIT 3;

Tasks
  1. Read payment.csv with read_csv() (copy it from g2).
  2. Build a dict { (customer_id, "YYYY-MM"): total } where total is a Decimal.
  3. Return the top 3 as a list of ((customer_id, month), total) pairs, biggest first.

Hints
  * The month is the first 7 characters of "2005-07-08 07:33:56" -> slicing [:7]
  * A tuple can be a dict key:  totals[(cid, month)]
  * Start each total at Decimal("0"):  totals.get(key, Decimal("0")) + Decimal(row["amount"])
  * Sort a dict by its values:  sorted(d.items(), key=lambda kv: kv[1], reverse=True)

Run:  uv run python lessons/week1/s2_monthly_totals.py
"""

from decimal import Decimal
from pathlib import Path
import csv

DATA_DIR = Path(__file__).resolve().parent / "data" 
payments_path = DATA_DIR / "payments.csv"

with open(payments_path, newline="", encoding="utf-8") as f:
    payment_list = list(csv.DictReader(f))

payments_totals = {}

for row in payment_list:
    cid = row["customer_id"]
    month = row["payment_date"][:7]
    amount = Decimal(row["amount"])
    payments_totals[(cid, month)] = payments_totals.get((cid, month), Decimal("0")) + amount

# print(payments_totals["148", "2005-07"])

def top_customer_months(n: int = 3) -> list[tuple[tuple[str, str], Decimal]]:
     """Return the n biggest (customer_id, month) totals, biggest first."""
     pairs = list(payments_totals.items())
     pairs_sorted = sorted(pairs, key=lambda kv: kv[1], reverse=True)

     return pairs_sorted[:n]

# ---------------- self-check (don't edit below) ----------------
expected = [
    (("148", "2005-07"), Decimal("100.78")),
    (("470", "2005-07"), Decimal("96.83")),
    (("522", "2005-07"), Decimal("96.82")),
]
got = top_customer_months(3)
# print(got)
print("PASS" if got == expected else f"FAIL  got {got!r}\n      expected {expected!r}")
