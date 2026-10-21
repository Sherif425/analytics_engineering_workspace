import csv
from pathlib import Path
from datetime import datetime
from decimal import Decimal, InvalidOperation

DATA_DIR = Path(__file__).resolve().parent / "data"

def read_csv(path: Path) -> list[dict[str,str]]:
    """ Read a CSV file into a list of dicts (one dict per row)."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check_payment(row: dict[str, str], valid_rental_ids: set[str]) -> list[str]:
    """ Returns a list of problems for one payment row ([] means valid). """
    problems = []

    # Rule 1 - Required
    if row["payment_id"] == "":
        problems.append("payment_id is empty")

    # Rule 2 + 3 - type, then range (only if the type was OK)
    try:
        amount = Decimal(row["amount"])
    except InvalidOperation:
        problems.append(f"amount {row['amount']!r} is not a number")
    else:
            if amount < 0:
                problems.append(f"amount {amount} is negative")
    
    try:
            datetime.fromisoformat(row["payment_date"])
    except ValueError:
            problems.append(f"payment_date {row['payment_date']!r} is not a date ")

    # Rule 4 - reference: rental_id must exist in rental.csv
    if row["rental_id"] == "":
            problems.append("rental_id is empty")
    elif row["rental_id"] not in valid_rental_ids:
            problems.append(f"rental_id {row['rental_id']} not found in rental")     

    return problems

# --- 1. See every rule fire on hand-made bad rows -----------------------------
print("1) hand-made rows, one problem each")
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


# ---- 2. Run the same rules on the real payment.csv
print("\n2) Real data: payment.csv")
rentals = read_csv(DATA_DIR / "rentals.csv")
payments = read_csv(DATA_DIR / "payments.csv")
rental_ids = {r["rental_id"] for r in rentals}

seen_ids: set[str] = set()
bad_rows = 0
for line_no, row in enumerate(payments, start=2):
    problems = check_payment(row, rental_ids)

    if row["payment_id"] in seen_ids:
        problems.append(f"payment_id {row['payment_id']} is a duplicate ")
    seen_ids.add(row["payment_id"])

    if problems:
         bad_rows += 1
         print(f"   line {line_no}:  {problems}")

print(f"    Checked {len(payments)} rows,  {bad_rows} with problems")
