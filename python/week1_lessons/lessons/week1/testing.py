from pathlib import Path
import csv
from collections import Counter



# current_dir = Path(__file__).resolve()
# current_working_dir = Path(__file__).cwd()

# print(f"This script file: {current_dir}, Current Working Directory : {current_working_dir}")

# # up two folders
# Project_DIR = Path(__file__).resolve().parent
# print(f"Project Directory: {Project_DIR}")
# Project_Data = Project_DIR / "data" / "payments.csv"
# print(f"Project Data: {Project_Data}")



# # with open(Project_Data, 'r') as file:
# #     reader = csv.DictReader(file)
# #     for row in reader:
# #         print(row)

# print("\n ")
# print(f"Project Data : f{Project_Data}")
# print("\n  .name  ", Project_Data.name) # payments.csv
# print("\n  .stem  ", Project_Data.stem) # payments
# print("\n  .suffix  ", Project_Data.suffix) # .csv   
# print("\n  .parent.name  ", Project_Data.parent.name) # data
# print("\n  .exists()  ", Project_Data.exists()) # True
# print("\n  .is_file()  ", Project_Data.is_file()) # True
# print("\n  .is_dir()  ", Project_Data.is_dir()) # False 


# for csv_path in sorted(current_working_dir.glob("*.csv")):
#     size_kb = csv_path.stat().st_size / 1024
#     print(f"   {csv_path.name:<20} {size_kb:8.1f} KB")

# REPORTS_DIR = Project_DIR / "reports"
# REPORTS_DIR.mkdir(parents=True, exist_ok=True)  # no error if it already exists
# print("\n5) Output folder ready:", REPORTS_DIR)


# dictRead
DATA_DIR = Path(__file__).resolve().parent / "data" 
# payments_path = DATA_DIR / "payments.csv"

# print("1) Header and first row")
# with open(payments_path, newline="", encoding="utf-8") as f:
#     reader =csv.DictReader(f)
#     print("    columns:", reader.fieldnames)
#     first_row = next(reader)
#     print("    first row:", first_row)


# print("4) Looping twice over the same reader")
# with open(payments_path, newline="", encoding="utf-8") as f:
#           reader = csv.DictReader(f)
#           first_pass = sum(1 for _ in reader)
#           second_pass = sum(1 for _ in reader)
#           print("    first pass:", first_pass)
#           print("    second pass:", second_pass)


# def read_csv(path: Path) -> list[dict[str, str]]:
#        with open(path, newline="", encoding="utf-8") as f:
#               return list(csv.DictReader(f))
       
# payments = read_csv(payments_path)
# print("\n payments file path: ", payments_path, "read_csv returned", len(payments), "rows")
# print("     last row: ", payments[-1])


# # -- empty string = NULL
# rental_path = DATA_DIR / "rentals.csv"
# rentals = read_csv(rental_path)
# print("rentals.csv file path: ", rental_path)
# print("    last row return date:  ", repr(rentals[-1]["return_date"]))
# print(" read_csv returned " , len(rentals), "rows")
# not_returned = [r for r in rentals if r["return_date"] == ""]

# print(not_returned)  
# print("\n Rentals with an empty return_date (never returned):", len(not_returned))
# print("    example: ", not_returned[0]["rental_id"], repr(not_returned[0]["return_date"]))


# #---- Looping with line numbers (useful for error messages later) ---------
# print("\n7) Line numbers: header is line 1, so the first data row is line 2 ")
# for line_no, row in enumerate(rentals[:3], start=2):
#     print(f"    line {line_no}: rental_id={row['rental_id']} customer_id={row['customer_id']}")
    
# for line_no, row in enumerate(rentals[:3], start=2):
#     print(f"    print(f"   line {line_no}: rental_id:{row[line_no]} customer_id: row["line_no "])   ")

#-----Try tis
def read_csv(path: Path) -> list[dict[str, str]]:
    """Read a CSV file into a list of dicts (one dict per row)."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
    
# customers_path = DATA_DIR / "customers.csv"
# customers = read_csv(customers_path)
# print("\n customers file path: ", customers_path, "read_csv returned", len(customers), "rows")
# print("    first customer email: ", customers[0]["email"])

# print("\n How many customers have active == 'true'?")
# active_customers = {int(r["customer_id"]) for r in customers if r["active"].strip().lower() == "true" } # returns a set shows the distinct values
# # print("    distinct active customer IDs:", active_customers)
# print("    active customers:", len(active_customers))


# g3_rows
# ---Self-test 1: load rental.csv into a list of dicts -----------------------
print("\n4) Self-test 1: load rental.csv into a list of dicts")
rentals = read_csv(DATA_DIR / "rentals.csv")
print("   read_csv() returned", len(rentals), "rows")  # self-test #1 doneread_csv
print("   last row:", rentals[-1])

counts: dict[str, int] = {}

for row in rentals:
    cid = row["customer_id"]
    counts[cid] = counts.get(cid, 0) + 1

print("\n2a) rentals for customer 148 (plain dict):", counts["148"])
