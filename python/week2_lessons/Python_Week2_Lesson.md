# Week 2 lesson: from drills to a tool (`validate_sakila.py`)

**Python for Data track · Py1 · restarted 18 Nov 2026 · about 5 hours over 2–3 sittings**

Builds on `Python_Week1_Wrapup_Lesson.md` (pathlib, `csv.DictReader`, row validation, logging).

## Warm-ups (closed notes, 15–20 min)

Do these on a blank file before reading further. If you can't, redo `g5_logging.py` and `s4` from week 1 first.

- **W1.** Write `read_csv(path)` from memory and print how many rows `rental.csv` has. Expect **16,044**.
- **W2.** Predict, then run. `row = {"amount": "2.99", "return_date": ""}`
  - (a) `row["amount"] * 2`
  - (b) `bool(row["return_date"])`
  - (c) `Decimal(row["amount"]) * 2`
- **W3.** Write the logging recipe from memory. Log one `INFO` line with the row count, and one `WARNING` for each rental with an empty `return_date`. Expect **183** warnings.

## Why week 2 exists

Week 1 scripts are read by you, on screen. From Phase 4 on, a script like this runs in Airflow at 3 a.m. and nobody reads the screen. So the script must:
1. tell a **bad row** apart from a **bad file**,
2. keep checking the other files when one is broken,
3. leave a **report** a machine can read,
4. say **pass or fail** with an exit code.

Each of the four ideas below solves one of these.

## Concept 1: two sizes of problem, and `raise`

| Size | Example | What to do |
|---|---|---|
| Row problem | `amount` is `"abc"` on line 425 | Record it in a list, keep going (week 1) |
| File problem | File missing, empty, or a column is missing | This file can't be checked at all, so stop checking *this file* |

In week 1 you **caught** exceptions that Python raised (`int("abc")` raises `ValueError`). Now you **raise your own**. A custom exception is a class with one line:

```python
class SchemaError(Exception):
    """The whole file can't be validated."""
```

`raise SchemaError("...")` stops the function immediately and hands the problem to whoever called it. Think of it as `exit 1` inside a function, except the caller decides what happens next.

```python
def read_checked(path: Path, expected: list[str]) -> list[dict[str, str]]:
    if not path.exists():
        raise SchemaError(f"{path.name}: file not found")
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:          # no header at all = empty file
            raise SchemaError(f"{path.name}: file is empty")
        missing = set(expected) - set(reader.fieldnames)
        if missing:
            raise SchemaError(f"{path.name}: missing columns {sorted(missing)}")
        return list(reader)
```

`reader.fieldnames` is the header row as a list, or `None` when the file is completely empty. The set subtraction is the set skill from your warm-ups.

## Concept 2: one bad file doesn't stop the others

Put the `try` around **one file**, inside the loop:

```python
for name, columns in EXPECTED.items():
    try:
        rows = read_checked(DATA_DIR / f"{name}.csv", columns)
    except SchemaError as e:
        log.error(e)
        results[name] = {"status": "error", "error": str(e)}
        continue                     # go to the next file
    # ... validate rows here ...
```

Catch **only `SchemaError`**, never a bare `except:`. If you make a typo in your own code, Python raises `NameError`, and you want that to crash loudly. A bare `except` would hide your bug and report it as a "file problem".

## Concept 3: a JSON report

JSON is dicts and lists written as text, so any tool (Airflow, a dashboard, `jq`) can read it.

```python
with open(REPORT_DIR / f"validation_{date.today()}.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
```

JSON only knows `str`, `int`, `float`, `bool`, `None`, `list` and `dict`. A `Decimal` or `datetime` inside `results` raises `TypeError: Object of type Decimal is not JSON serializable`. Convert those with `str()` first.

## Concept 4: exit codes

You know this from shell: `$?` is `0` for success and non-zero for failure. Cron, CI and Airflow all read it. In Python:

```python
sys.exit(0)   # or 1, or 2
```

Our rule:

| Code | Meaning |
|---|---|
| `0` | Every file read, no row problems |
| `1` | Every file read, but some rows have problems |
| `2` | At least one file couldn't be checked |

Check it with `uv run python validate_sakila.py; echo $?`.

## Practice: build `validate_sakila.py` in 4 steps

Run the script after each step. Commit on a branch: `git switch -c week2-validate`.

**Step 1: read with file checks (1 h).**
- Make an `EXPECTED` dict for `rental`, `payment` and `customer`, mapping each table to the columns your rules need.
- Write `SchemaError` and `read_checked`.
- Loop over the tables and log `"rental: read 16044 rows"`.

**Step 2: row checks (1–1.5 h).**
- Plug in your week 1 validators: one function per table that takes a row and returns a list of problem strings, plus the uniqueness check.
- Store per table: `status`, `rows`, `problem_count` and the first 20 problems.

**Step 3: report (30 min).** Write the JSON report to `reports/`. Open it and check that it's readable.

**Step 4: exit code (20 min).** Exit `0`, `1` or `2` using the rule above.

**Bonus: test folder from the command line.** Let the script take an optional folder: `DATA_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DIR`. `sys.argv[1]` is Python's `$1`.

## "What would break it?" checklist

Copy the CSVs to a scratch folder, so your real data stays clean: `cp -r data/sakila_csv /tmp/broken`. For each case, **predict** the log lines and exit code, then run `uv run python validate_sakila.py /tmp/broken; echo $?`.

1. Empty `payment.csv` (`: > /tmp/broken/payment.csv`)
2. `customer.csv` with only the header line
3. `rental.csv` with the `customer_id` column deleted
4. One `payment.csv` row where `amount` is `abc`
5. One duplicated `rental_id`
6. `customer.csv` deleted

Case 2 is a decision for you, not a bug: is a file with a header but zero rows a file problem or fine? Write down your choice and why.

## Done when

- [ ] W1–W3 done from memory.
- [ ] Real Sakila data gives no file errors. Any row problems are ones you can explain (for example, Sakila really has 183 rentals with no `return_date`; that's a valid NULL, not an error).
- [ ] All 6 broken cases give the exit code you predicted, and the other files are still checked.
- [ ] `reports/` and `logs/` are in `.gitignore`; branch merged.
- [ ] Paste the script for review: "What would break with an empty file or a bad row?" (tutor mode, no rewrite).

## What's next: week 3 content (APIs)

`requests`, sessions, retries with backoff, pagination, secrets in env vars, building the Open-Meteo extractor v1. That's the first piece of the Gate 1 test.
