import csv
from collections import Counter


with open("data/sakila_csv/rental.csv", "r") as f:
    reader = list(csv.DictReader(f))
    print(type(reader ))

customer_count = len(set(row["customer_id"] for row in reader))
print(f"Number of unique customers: {customer_count}")

customer_count_2 = Counter(row["customer_id"] for row in reader)
print(f"Number of unique customers (using Counter): {len(customer_count_2)}")