import csv
from collections import Counter
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data" 
print(DATA_DIR)

def read_csv(path: Path) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
    
# load rentals.csv and customers.csv files 
rentals = read_csv(DATA_DIR / "rentals.csv")
customers = read_csv(DATA_DIR / "customers.csv")

print(f"loaded {len(rentals)} rentals and {len(customers)} customers")

# Top 5 customers by number of rentals; the plain-loop way
counts: dict[str, int] = {}
for row in rentals:
    cid = row["customer_id"]
    counts[cid] = counts.get(cid, 0) + 1 
print("Rentals for customer 150 (plain dict):", counts["150"])

# Top 5 customers ; the Counter way
rentals_counts = Counter(row["customer_id"] for row in rentals)
print("Rentals for custoemrs 150 (Coutner): " , rentals_counts["150"])

for cid, n in rentals_counts.most_common(5):
    print(f"Customer {cid:>3}: {n} rentals")

