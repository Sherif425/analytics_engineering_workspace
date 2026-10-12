# SOLO 5: explain it in your own words (self-test 6)

Write 2–4 sentences per question under each one, without looking anything up. Then paste the file to Claude for review.

## Predict, then run

Write down what you think each snippet prints, and only then run it in `uv run python`.

```python
a = [1, 2]
b = a
b.append(3)
print(a)          # prediction:
```

```python
a = [1, 2]
b = a.copy()
b.append(3)
print(a)          # prediction:
```

```python
row = {"amount": "2.99"}
print(row["amount"] * 2)    # prediction:
```

```python
totals = {}
totals[["148", "2005-07"]] = 100   # prediction (works or error? which error?):
```

## Explain

1. Why does `b = a; b.append(3)` also change `a`?

2. Why can a tuple be a dict key but a list can't?

3. Why is `x in big_set` faster than `x in big_list`?

4. Why do we build paths from `Path(__file__)` instead of writing `"data/sakila_csv/rental.csv"`?

5. Every value from `csv.DictReader` is a string. Name two bugs this causes if you forget it.

6. When do you use `log.warning` and when `log.error`? Give one Sakila example of each.

7. In g4, the 5 payments with an empty `rental_id`: would you treat them as an error or as a warning? Why?
