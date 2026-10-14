from pathlib import Path
import csv

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
payments_path = DATA_DIR / "payments.csv"

print("1) Header and first row")
with open(payments_path, newline="", encoding="utf-8") as f:
    reader =csv.DictReader(f)
    print("    columns:", reader.fieldnames)
    first_row = next(reader)
    print("    first row:", first_row)


print("4) Looping twice over the same reader")
with open(payments_path, newline="", encoding="utf-8") as f:
          reader = csv.DictReader(f)
          first_pass = sum(1 for _ in reader)
          second_pass = sum(1 for _ in reader)
          print("    first pass:", first_pass)
          print("    second pass:", second_pass)


def read_csv(path: Path) -> list[dict[str, str]]:
       with open(path, newline="", encoding="utf-8") as f:
              return list(csv.DictReader(f))
       
payments = read_csv(payments_path)
print("\n read_csv returned", len(payments), "rows")
print("     last row: ", payments[-1])