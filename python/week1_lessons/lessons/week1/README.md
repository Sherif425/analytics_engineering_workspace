# Week 1 wrap-up: files, CSV, validation, logging

**Python for Data track · Py1 · about 4–5 hours over 2–3 sittings**

This folder is your single path through four topics: **pathlib**, **csv.DictReader**, **row validation** and **logging**. When this lesson and a YouTube video disagree, follow this lesson for now. The videos aren't wrong; they're showing other valid styles. You'll recognise those styles once these basics are solid.

## How to use this folder

Put the `lessons/` folder in your `python/` project, next to `data/`. Run everything from the `python/` folder.

| Order | File | Type | Time |
|---|---|---|---|
| 0 | `00_warmup.py` | Warm-up: lists, dicts and sets you already know | 15 min |
| 1 | `g1_pathlib.py` | Guided: finding files | 30 min |
| 2 | `g2_dictreader.py` | Guided: CSV to dicts | 30 min |
| 3 | `g3_rows.py` | Guided: answering questions (self-tests 1–3) | 30 min |
| 4 | `g4_validation.py` | Guided: rules and try/except | 40 min |
| 5 | `g5_logging.py` | Guided: logging instead of print | 30 min |
| 6 | `s1` → `s5` | Solo drills with built-in PASS/FAIL checks | 1.5–2 h |

**How to work through a guided file:**
1. Read the CONCEPT block at the top.
2. Predict what the script will print.
3. Run it and compare with your prediction.
4. Do the TRY THIS items at the bottom.

**How to work through a solo file:** fill in the `# TODO` parts and run it until every line says `PASS`. Don't copy from the guided files. Reopen them to remind yourself of an idea, close them, then type your own version.

```bash
cd ~/analytics_engineering_workspace/python
uv run python lessons/week1/g1_pathlib.py
```

## The four concepts in plain words

### 1. Paths: where is the file?
A **relative path** like `data/sakila_csv/rental.csv` is relative to the folder your terminal is in, not the folder the script is in. Run the script from somewhere else and it breaks with `FileNotFoundError`. To avoid that, anchor every path to the script file itself and build the rest with `/`:

```python
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent   # up 3 levels from this file
DATA_DIR = PROJECT_ROOT / "data" / "sakila_csv"
```

**What you need to know:** `/` to join, `.exists()`, `.name`, `.stem`, `.suffix`, `.parent`, `.glob("*.csv")`, and `.mkdir(parents=True, exist_ok=True)`.

### 2. CSV to dicts: what's inside the file?
`csv.DictReader` gives you **one dict per row**, and the header row supplies the keys. Four facts explain most bugs:
1. Every value is a **string** (`"130"`, not `130`).
2. An empty cell (NULL) is `""`.
3. The reader can only be read **once**.
4. You must read it **inside** the `with` block, while the file is still open.

```python
def read_csv(path: Path) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
```

### 3. Validation: is each row correct?
A **rule** is a check on a row. There are five kinds:
- **required:** the value isn't empty
- **type:** it converts to the right type
- **range:** it makes business sense
- **reference:** the id exists in another table
- **unique:** no id appears twice

Type rules use `try` / `except`. You *try* the conversion, and if the text is bad Python *raises* an exception, which you *catch* and record as a problem instead of crashing.

The pattern: **one function per table that takes one row and returns a list of problem messages.** An empty list means the row is valid. The loop around it adds line numbers and runs the uniqueness check.

| Conversion | Error when the text is bad |
|---|---|
| `int("abc")` | `ValueError` |
| `datetime.fromisoformat("x")` | `ValueError` |
| `Decimal("abc")` (use this for money) | `decimal.InvalidOperation` |

### 4. Logging: what happened, and when?
`print` only puts text on the screen. `logging` adds a **timestamp** and a **level**, and can also write to a **file**.

| Level | Use it for |
|---|---|
| `DEBUG` | Details while you're developing (hidden by default) |
| `INFO` | Normal progress: "read 16049 rows" |
| `WARNING` | Something odd, but the run continues: "line 425: rental_id is empty" |
| `ERROR` | Something failed: "payment.csv not found" |

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(LOG_DIR / "app.log", encoding="utf-8")],
)
log = logging.getLogger(__name__)
```

This recipe is all the logging you need until week 22. You can skip anything about `dictConfig`, filters, custom handlers, propagation or logger hierarchies for now.

## The "one way" decisions

When sources disagree, these are the choices this lesson makes.

| Topic | We use | You may see elsewhere (ignore for now) |
|---|---|---|
| Paths | `pathlib.Path` anchored on `__file__` | `os.path.join`, plain strings |
| Opening files | `with open(path, newline="", encoding="utf-8")` | `open()` without `with`, `path.open()` |
| Reading CSV | `csv.DictReader` (pandas comes in week 4) | `csv.reader` with indexes, pandas |
| Money | `Decimal` | `float` |
| Dates | `datetime.fromisoformat` | `strptime` with format codes |
| Log messages | f-strings: `log.info(f"Read {n} rows")` | `log.info("Read %d rows", n)` (also fine) |
| Logging setup | `basicConfig` with 2 handlers | `dictConfig`, YAML config, loguru |

## Done when
- [ ] `00_warmup.py` and `s1`–`s4` print only `PASS`.
- [ ] `s5_explain.md` is answered and reviewed with Claude.
- [ ] You can write `read_csv()` and the logging recipe from memory on a blank file.
- [ ] `logs/` and `reports/` are in `.gitignore`. Commit on a branch, then merge: `git switch -c week1-lessons`.

## What's next: Week 2 (Files, errors, logging)
You'll already have the basics, so Week 2 builds **one real tool** instead of drills. New ideas you'll learn there:
- Writing **JSON** (a summary report) with `json.dump`.
- **Raising** your own exceptions (`raise SchemaError(...)`) when a whole file is wrong, not just a row.
- **Exit codes**: the script tells a scheduler (later, Airflow) whether it passed.
- Checking **several files** in one run without one bad file stopping the others.

The output is `validate_sakila.py`, the Week 2 practice from your track document.
