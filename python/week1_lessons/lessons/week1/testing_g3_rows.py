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
# rentals_counts = Counter(row["customer_id"] for row in rentals)
# print("Rentals for custoemrs 150 (Coutner): " , rentals_counts["150"])

# for cid, n in rentals_counts.most_common(5):
#     print(f"Customer {cid:>3}: {n} rentals")

rentals_count = Counter(row["customer_id"] for row in rentals)
print(rentals_count, type(rentals_count))

print("Rentals for customer 148 : ", rentals_count["148"])
for cid, n in rentals_count.most_common(5):
    print(f"Customer {cid: >3}: {n} rentals")

# Step C: make it readable with a lookup dict {customer_id: full name} (=JOIN)
# name_by_id = {c["customer_id"]: f"{c['first_name']} {c['last_name']}" for c in customers}

# for cid, n in rentals_count.most_common(5):
#     print(f"   {name_by_id[cid]:<22} {n} rentals")

name_by_id = {c["customer_id"]:f"{c['first_name']} {c['last_name']}" for c in customers}
# print(name_by_id)

for cid, n in rentals_count.most_common(5):
    print(f"   {name_by_id[cid]:<22} {n} rentals")


# Customer_ids in rental that are missing from customers
rental_customer_ids = {row["customer_id"] for row in rentals}  # set = DISTINCT
known_customer_ids = {c["customer_id"] for c in customers}
orphans = rental_customer_ids - known_customer_ids   # set difference = EXCEPT
print("\n3) Distinct customers in rental:", len(rental_customer_ids))
print("    Orphan customer_ids (in rental, not in customer):", orphans or "none")
#---------------------------------
# a) Top 3 inventory_ids by number of rentals.
inventory = read_csv(DATA_DIR / "inventory.csv")

inventory_counts = Counter(row["inventory_id"] for row in rentals)
for inv_id, n in inventory_counts.most_common(3):
    print(f"Inventroy {inv_id:>4}: {n} rentals ")

# b) Which customers have NEVER rented anything?  (known_customer_ids - rental_customer_ids)
customers_never_rented = known_customer_ids.difference(rental_customer_ids )

print("Customers never rented anything: ", customers_never_rented)

# c) Count rentals per staff_id with Counter.
rentals_per_staff_id = Counter(row["staff_id"] for row in rentals)
for staff_id, n in rentals_per_staff_id.most_common():
    print(f"Staff {staff_id}:  {n} rentals")
