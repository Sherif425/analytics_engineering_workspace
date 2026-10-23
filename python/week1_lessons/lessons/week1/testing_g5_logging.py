import csv
import logging
from pathlib import Path
from datetime import datetime
from decimal import Decimal, InvalidOperation

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

#----The Recipe
logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / "wee1.log", encoding= "utf-8"),
    ]
)
log =logging.getLogger(__name__)

# --- The Four levels
log.debug("1) you will NOT see this: DEBUG is below INFO")
log.info("1) INFO: normal progress")
log.warning("1) WARNING: odd, but we continue")
log.error("1) ERROR: something failed")

# --- 2. Logging inside a real flow ---------------------------------------------
def read_csv(path) -> list[dict[str, str]]:
    with open(path, newline = "", encoding = "utf-8") as f:
        return list(csv.DictReader(f))


def validate_amounts(path: Path) -> int:
    if not path.exists():
        log.error(f"{path.name} not found in the path: {path.parent}")
        return -1

    rows = read_csv(path)
    log.info(f"Read {len(rows)} rows from {path.name} ")

    bad = 0
    for line_no, row in enumerate(rows, start =2):
        try:
            amount = Decimal(row["amount"])
        except InvalidOperation:
            log.warning(f"{path.name} line {line_no}: amount {row['amount']} is not a number")    
            bad += 1
            continue
        if amount  < 0:
            log.warning(f"{path.name} line {line_no}: amount {amount} is negative")
            bad += 1

    log.info(f"{path.name}: {len(rows) - bad} valid, {bad} invalid")
    return bad


validate_amounts(DATA_DIR / "payment.csv")
validate_amounts(DATA_DIR / "payments.csv")


