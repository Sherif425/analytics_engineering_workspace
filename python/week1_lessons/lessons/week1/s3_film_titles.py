"""SOLO 3 - joining with lookup dicts (self-test 5; uses: g3).

Goal: the film title of rentals with rental_id 1, 2, 3, 4, 5.

A rental doesn't know its film. The chain is:
    rental.inventory_id -> inventory.film_id -> film.title

SQL you'd write:
    SELECT r.rental_id, f.title
    FROM rental r
    JOIN inventory i ON i.inventory_id = r.inventory_id
    JOIN film f      ON f.film_id = i.film_id
    WHERE r.rental_id IN (1,2,3,4,5) ORDER BY r.rental_id;

Tasks
  1. Build film_title  = {film_id: title}           from film.csv
  2. Build film_of_inv = {inventory_id: film_id}    from inventory.csv
  3. For rentals with rental_id "1".."5" (in that order), look up the title
     through both dicts. Return the list of 5 titles.

Hint: remember ids are STRINGS in the CSV: compare with "1", not 1.

Run:  uv run python lessons/week1/s3_film_titles.py
"""

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "sakila_csv"


def titles_for_rentals(rental_ids: list[str]) -> list[str]:
    # TODO
    return []


# ---------------- self-check (don't edit below) ----------------
expected = ["BLANKET BEVERLY", "FREAKY POCUS", "GRADUATE LORD", "LOVE SUICIDES", "IDOLS SNATCHERS"]
got = titles_for_rentals(["1", "2", "3", "4", "5"])
print("PASS" if got == expected else f"FAIL  got {got!r}\n      expected {expected!r}")
