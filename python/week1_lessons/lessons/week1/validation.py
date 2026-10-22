import csv
from pathlib import Path
from datetime import datetime
from decimal import Decimal, InvalidOperation

MAX_AMOUNT = Decimal("20.00")
DATA_DIR = Path(__file__).resolve().parent / "data"

def read_csv(path: Path) -> list[dict[str, str]]:
    """ Read a csv file into a list of dicts (one dict per row)"""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check_uniquness(row: dict[str, str], seen_ids: set[str]) -> list[str]:
    """ Returns a problem if this payment_id was seen before; remember it either way"""
    problems = []
   
    if row["payment_id"] in seen_ids:
        problems.append(f"payment_id {row['payment_id']} is a duplicate")
    seen_ids.add(row["payment_id"])
    return problems

def check_payment(row: dict[str, str], valid_rental_ids: set[str]) -> list[str]:
    """ Return a list of problems for one payment row ([] means valid)."""
    problems = []

    # Rule 1 - required
    if row["payment_id"] == "":
        problems.append("payment_id is empty")
    # Rule 2 + 3 - type, then range (only if the type was OK)
    try:
        amount = Decimal(row["amount"])
    except InvalidOperation:
        problems.append(f"amount {row['amount']!r} is not a number")
    else:
        if amount < 0 :
            problems.append(f"amount {amount} is negative")
        elif amount > MAX_AMOUNT:
            problems.append(f"amount is above {MAX_AMOUNT}")            

    try:
        payment_date = datetime.fromisoformat(row["payment_date"])
    except ValueError:
        problems.append(f"payment_date {row['payment_date']!r} is not a date")
    else:
        if payment_date.year not in {2005, 2006}:
            problems.append(f"payment_date {row['payment_date']} is outside 2005-2006 ")
    
    
    
    # Rule 4 - Refernece: rental_id must exist in rental.csv
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
    print(f"    payment_id={row['payment_id']!r:6} -> {check_payment(row, VALID_RENTALS) or 'OK'}")

# --- 2. Run the same rules on the real payment.csv ------------------------------
print("\n2) Real data: payments.csv")
rentals = read_csv(DATA_DIR / "rentals.csv")
payments = read_csv(DATA_DIR / "payments.csv")
rental_ids = {r["rental_id"] for r in rentals}

seen_ids: set[str] = set()
bad_rows = 0
for line_no, row in enumerate(payments, start=2):
    problems = check_payment(row, rental_ids)

for line_no, row in enumerate(payments, start =2):
    problems = check_uniquness(row, seen_ids)

    if problems:
        bad_rows += 1
        print(f"   line {line_no}: {problems}")
print(f"   checked {len(payments)} rows, {bad_rows} with problems")


# Try THIS
