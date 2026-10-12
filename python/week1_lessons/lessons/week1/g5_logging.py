"""GUIDED 5 - logging instead of print.

CONCEPT
-------
print() writes text to the screen. That's all it does. A real pipeline needs to know:
  * WHEN did it happen?           -> a timestamp on every line
  * HOW SERIOUS is it?            -> a level
  * WHERE is it kept?             -> screen AND a file you can read tomorrow

The logging module does all three. The levels, from least to most serious:
  DEBUG    details for you while developing         (hidden by default)
  INFO     normal progress: "read 16049 rows"
  WARNING  something odd, but the run continues     "line 425: rental_id is empty"
  ERROR    something failed                          "payment.csv not found"
You choose a minimum level; anything below it is not shown.

Three words you'll meet everywhere:
  * logger  - the object you call:          log.info("...")
  * handler - WHERE the messages go:        the screen (StreamHandler), a file (FileHandler)
  * format  - WHAT each line looks like:    time, level, message

THE ONE RECIPE WE USE (until week 22, ignore everything else about logging)
-------------------------------------------------------------------------
    logging.basicConfig(level=..., format=..., handlers=[...])   # once, at the start
    log = logging.getLogger(__name__)                             # in every file
    log.info(...) / log.warning(...) / log.error(...)
Gotcha: basicConfig only works the FIRST time it is called in a program.

Run:   uv run python lessons/week1/g5_logging.py
Then:  cat logs/week1.log
"""

import csv
import logging
from decimal import Decimal, InvalidOperation
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "sakila_csv"
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

# --- The recipe ----------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,  # show INFO and above
    format="%(asctime)s %(levelname)-8s %(message)s",
    handlers=[
        logging.StreamHandler(),  # -> the screen
        logging.FileHandler(LOG_DIR / "week1.log", encoding="utf-8"),  # -> a file
    ],
)
log = logging.getLogger(__name__)

# --- 1. The four levels ------------------------------------------------------
log.debug("1) you will NOT see this: DEBUG is below INFO")
log.info("1) INFO: normal progress")
log.warning("1) WARNING: odd, but we continue")
log.error("1) ERROR: something failed")


# --- 2. Logging inside a real flow ---------------------------------------------
def read_csv(path: Path) -> list[dict[str, str]]:
    """Read a CSV file into a list of dicts (one dict per row)."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_amounts(path: Path) -> int:
    """Log one WARNING per bad amount; return the number of bad rows."""
    if not path.exists():
        log.error(f"{path.name} not found in {path.parent}")
        return -1

    rows = read_csv(path)
    log.info(f"Read {len(rows)} rows from {path.name}")

    bad = 0
    for line_no, row in enumerate(rows, start=2):
        try:
            amount = Decimal(row["amount"])
        except InvalidOperation:
            log.warning(f"{path.name} line {line_no}: amount {row['amount']!r} is not a number")
            bad += 1
            continue  # skip to the next row
        if amount < 0:
            log.warning(f"{path.name} line {line_no}: amount {amount} is negative")
            bad += 1

    log.info(f"{path.name}: {len(rows) - bad} valid, {bad} invalid")
    return bad


validate_amounts(DATA_DIR / "payment.csv")  # real file: all amounts are fine
validate_amounts(DATA_DIR / "payments.csv")  # typo on purpose -> ERROR, no crash

# --- 3. Logging an unexpected crash with its traceback ------------------------
try:
    int("not a number")
except ValueError:
    log.exception("3) log.exception = ERROR + the full traceback, use it inside except")

log.info(f"Done. Full log written to {LOG_DIR / 'week1.log'}")

# TRY THIS
# a) Change level=logging.INFO to logging.DEBUG. What appears now?
# b) Change level to logging.WARNING. Which lines disappear?
# c) Run the script twice, then: cat logs/week1.log
#    The file keeps growing (append mode). The screen does not keep history.
# d) Add "logs/" and "reports/" to .gitignore. Logs are output, not code.
