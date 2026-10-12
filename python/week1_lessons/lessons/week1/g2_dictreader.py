"""GUIDED 2 - csv.DictReader: turning a CSV file into dictionaries.

CONCEPT
-------
A CSV file is just text. Line 1 is the header (column names), every other line
is one row. csv.DictReader reads it and gives you ONE DICT PER ROW:

    rental_id,rental_date,inventory_id,customer_id,...     <- header = the keys
    1,2005-05-24 22:53:30,367,130,...                      <- {"rental_id": "1", ...}

Four facts that explain almost every beginner bug:
  1. Every value is a STRING. "130" is not 130. You convert it yourself.
  2. An empty cell (NULL in the database) is the empty string "".
  3. The reader is a one-way stream: once you've looped over it, it is empty.
  4. The file must stay open while you read -> do the reading INSIDE "with".

"with open(...) as f:" is a context manager: it opens the file, and closes it
automatically when the block ends, even if an error happens inside.

THE ONE PATTERN WE USE
----------------------
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
newline=""  -> let the csv module handle line endings (official recommendation)
encoding    -> always say it; don't depend on the machine's default

Run:   uv run python lessons/week1/g2_dictreader.py
"""

import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "sakila_csv"
rental_path = DATA_DIR / "rental.csv"

# --- 1. Open, look at the header and the first row ---------------------------
print("1) Header and first row")
with open(rental_path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    print("   columns:", reader.fieldnames)
    first_row = next(reader)  # next() takes ONE row from the stream
    print("   first row:", first_row)

# --- 2. Every value is a string ---------------------------------------------
print("\n2) Values are strings")
print("   type of rental_id:", type(first_row["rental_id"]))
print('   "10" + "5"         =', "10" + "5")  # text glued together
print("   int('10') + int('5') =", int("10") + int("5"))  # real numbers

# --- 3. The file is closed after the with-block -------------------------------
print("\n3) After the with-block the file is closed:", f.closed)

# --- 4. The reader is a one-way stream ----------------------------------------
print("\n4) Looping twice over the same reader")
with open(rental_path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    first_pass = sum(1 for _ in reader)
    second_pass = sum(1 for _ in reader)  # already at the end of the file
print(f"   first loop counted {first_pass} rows, second loop counted {second_pass}")
print("   -> if you need the rows more than once, store them: rows = list(reader)")


# --- 5. The reusable function you will use from now on ------------------------
def read_csv(path: Path) -> list[dict[str, str]]:
    """Read a CSV file into a list of dicts (one dict per row)."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


rentals = read_csv(rental_path)
print("\n5) read_csv() returned", len(rentals), "rows")  # self-test #1 done
print("   last row:", rentals[-1])

# --- 6. Empty string = NULL ----------------------------------------------------
not_returned = [r for r in rentals if r["return_date"] == ""]
print("\n6) Rentals with an empty return_date (never returned):", len(not_returned))
print("   example:", not_returned[0]["rental_id"], repr(not_returned[0]["return_date"]))

# --- 7. Looping with line numbers (useful for error messages later) ---------
print("\n7) Line numbers: header is line 1, so the first data row is line 2")
for line_no, row in enumerate(rentals[:3], start=2):
    print(f"   line {line_no}: rental_id={row['rental_id']} customer_id={row['customer_id']}")

# TRY THIS
# a) Read customer.csv with read_csv() and print the first customer's email.
# b) How many customers have active == "1"? Look at the values first:
#    print({r["active"] for r in customers})  -> a set shows the distinct values.
# c) Remove newline="" and encoding="utf-8". It still works here, so why keep them?
#    (Answer: CSVs with line breaks inside quoted text, and non-English letters,
#     break without them. The pattern is safe everywhere, so we always use it.)
