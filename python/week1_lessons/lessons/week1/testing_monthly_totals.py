from decimal import Decimal

totals = {("1", "2005-05"): Decimal("3.98"),
          ("2", "2005-05"): Decimal("9.50"),
          ("1", "2005-06"): Decimal("5.99")}

pairs = list(totals.items())

for pair in pairs:
    print(pair[0])

def get_total(pair):
    return pair[1]

sorted_pairs = sorted(pairs, key= lambda kv:kv[1], reverse=True)

print(sorted_pairs)