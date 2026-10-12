"""GUIDED 4 - Validating each row.

CONCEPT
-------
Validation = checking every row against RULES, and collecting the problems
instead of crashing on the first one. Four kinds of rules cover most cases:

  1. Required   - the value is not empty                 row["payment_id"] != ""
  2. Type       - the text converts to the right type    int("abc") fails
  3. Range      - the value makes business sense         amount >= 0
  4. Reference  - the id exists in another table         rental_id in rental ids
  (+ Unique     - no id appears twice                    keep a set of seen ids)

Type rules use try / except:
  * You TRY the conversion.
  * If the text is bad, Python RAISES an exception (an error object).
  * EXCEPT catches that specific error, and you record a problem instead of crashing.
      int("abc")                 -> ValueError
      datetime.fromisoformat("x") -> ValueError
      Decimal("abc")             -> decimal.InvalidOperation
  Money uses Decimal, not float: float(0.1 + 0.2) is 0.30000000000000004.

THE ONE PATTERN WE USE
----------------------
One function per table that takes ONE row and returns a LIST OF PROBLEM MESSAGES.
Empty list = the row is valid. The caller loops over rows and adds line numbers.

Run:   uv run python lessons/week1/g4_validation.py
"""

import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "sakila_csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read a CSV file into a list of dicts (one dict per row)."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check_payment(row: dict[str, str], valid_rental_ids: set[str]) -> list[str]:
    """Return a list of problems for one payment row ([] means valid)."""
    problems = []

    # Rule 1 - required
    if row["payment_id"] == "":
        problems.append("payment_id is empty")

    # Rule 2 + 3 - type, then range (only if the type was OK)
    try:
        amount = Decimal(row["amount"])
    except InvalidOperation:
        problems.append(f"amount {row['amount']!r} is not a number")
    else:  # "else" runs only when the try-block raised nothing
        if amount < 0:
            problems.append(f"amount {amount} is negative")

    try:
        datetime.fromisoformat(row["payment_date"])
    except ValueError:
        problems.append(f"payment_date {row['payment_date']!r} is not a date")

    # Rule 4 - reference: rental_id must exist in rental.csv
    if row["rental_id"] == "":
        problems.append("rental_id is empty")
    elif row["rental_id"] not in valid_rental_ids:
        problems.append(f"rental_id {row['rental_id']} not found in rental")

    return problems


# --- 1. See every rule fire on hand-made bad rows -----------------------------
print("1) Hand-made rows, one problem each")
VALID_RENTALS = {"1", "2", "3"}
test_rows = [
    {"payment_id": "1", "amount": "2.99", "payment_date": "2005-05-25 11:30:37", "rental_id": "1"},
    {"payment_id": "", "amount": "2.99", "payment_date": "2005-05-25 11:30:37", "rental_id": "1"},
    {"payment_id": "3", "amount": "abc", "payment_date": "2005-05-25 11:30:37", "rental_id": "2"},
    {"payment_id": "4", "amount": "-5.00", "payment_date": "2005-05-25 11:30:37", "rental_id": "2"},
    {"payment_id": "5", "amount": "1.99", "payment_date": "25/05/2005", "rental_id": "3"},
    {"payment_id": "6", "amount": "1.99", "payment_date": "2005-05-25 11:30:37", "rental_id": "999"},
]
for row in test_rows:
    print(f"   payment_id={row['payment_id']!r:6} -> {check_payment(row, VALID_RENTALS) or 'OK'}")

# --- 2. Run the same rules on the real payment.csv ------------------------------
print("\n2) Real data: payment.csv")
rentals = read_csv(DATA_DIR / "rental.csv")
payments = read_csv(DATA_DIR / "payment.csv")
rental_ids = {r["rental_id"] for r in rentals}

seen_ids: set[str] = set()  # for the "unique" rule
bad_rows = 0
for line_no, row in enumerate(payments, start=2):  # line 1 is the header
    problems = check_payment(row, rental_ids)

    # Unique rule needs memory of earlier rows, so it lives in the loop
    if row["payment_id"] in seen_ids:
        problems.append(f"payment_id {row['payment_id']} is a duplicate")
    seen_ids.add(row["payment_id"])

    if problems:
        bad_rows += 1
        print(f"   line {line_no}: {problems}")

print(f"   checked {len(payments)} rows, {bad_rows} with problems")

# Those 5 rows are REAL: Sakila has payments with no rental_id.
# Is that an error (stop the pipeline) or a warning (load, but flag it)?
# That is a business decision, not a Python one. You'll make it in Week 2.

# TRY THIS
# a) Add a rule: amount must be <= 20.00 (no rental costs more). Does real data pass?
# b) Add a rule: payment_date must be in 2005 or 2006.
#    Hint: datetime.fromisoformat(...).year
# c) Move the unique rule into a function. What would it need as an extra argument?
