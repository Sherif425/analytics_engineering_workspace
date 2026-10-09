"""Copy Sakila from MySQL into DuckDB, then export every table to CSV.

Usage (from your template repo root, after `uv add duckdb`):
    export MYSQL_PWD=sakila          # Windows PowerShell: $env:MYSQL_PWD="sakila"
    uv run python build_sakila.py

Creates:
    data/sakila.duckdb
    data/sakila_csv/<table>.csv   (16 files)
"""

import logging
import os
from pathlib import Path

import duckdb

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("build_sakila")

TABLES = [
    "actor", "address", "category", "city", "country", "customer", "film",
    "film_actor", "film_category", "film_text", "inventory", "language",
    "payment", "rental", "staff", "store",
]
# address.location is a MySQL GEOMETRY column; DuckDB can't read it, and we don't need it.
EXCLUDE = {"address": ["location"]}

DATA = Path("data")
DB_PATH = DATA / "sakila.duckdb"
CSV_DIR = DATA / "sakila_csv"


def main() -> None:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    host = os.getenv("MYSQL_HOST", "127.0.0.1")
    port = os.getenv("MYSQL_PORT", "3306")
    user = os.getenv("MYSQL_USER", "dbadmin")
    password = os.environ["MYSQL_PWD"]  # never hard-code secrets

    con = duckdb.connect(str(DB_PATH))
    con.execute("INSTALL mysql; LOAD mysql;")
    con.execute(
        f"ATTACH 'host={host} port={port} user={user} password={password} database=sakila' "
        "AS src (TYPE mysql, READ_ONLY)"
    )

    for table in TABLES:
        cols = "*"
        if table in EXCLUDE:
            cols = f"* EXCLUDE ({', '.join(EXCLUDE[table])})"
        con.execute(f"CREATE OR REPLACE TABLE main.{table} AS SELECT {cols} FROM src.{table}")
        rows = con.execute(f"SELECT count(*) FROM main.{table}").fetchone()[0]
        csv_path = CSV_DIR / f"{table}.csv"
        con.execute(f"COPY main.{table} TO '{csv_path.as_posix()}' (HEADER, DELIMITER ',')")
        log.info("%-14s %6d rows -> %s", table, rows, csv_path)

    con.execute("DETACH src")
    con.close()
    log.info("Done: %s and %d CSVs in %s", DB_PATH, len(TABLES), CSV_DIR)


if __name__ == "__main__":
    main()
