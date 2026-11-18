# Loading Sakila (16 tables) from MySQL into DuckDB

## The idea

DuckDB can **ATTACH** a running MySQL database, like mounting a filesystem in Linux: the data becomes reachable, but nothing is copied yet. You then copy the tables into a local DuckDB file.

| Part | What it does |
|---|---|
| `duckdb sakila.duckdb` | Creates or opens a DuckDB file. The database inside it is named `sakila`, after the file name. |
| `INSTALL mysql; LOAD mysql;` | Adds the MySQL extension to DuckDB. |
| `ATTACH '...' AS src (TYPE mysql, READ_ONLY)` | Connects to MySQL as a database called `src`. `READ_ONLY` makes sure DuckDB can't change MySQL. |
| `COPY FROM DATABASE src TO sakila` | Copies all tables, with structure and data, from `src` into the DuckDB file. |

> Use `host=127.0.0.1`, not `localhost`. With `localhost`, MySQL clients try the Unix socket instead of TCP, which often fails when MySQL runs in Docker.

---

## Option 1: copy everything in one statement

```bash
duckdb sakila.duckdb -c "INSTALL mysql; LOAD mysql; ATTACH 'host=127.0.0.1 port=3306 user=root password=YOURPASS database=sakila' AS src (TYPE mysql, READ_ONLY); COPY FROM DATABASE src TO sakila;"
```

**Catch:** Sakila also has 7 views (`customer_list`, `film_list`, `sales_by_store`, and others). Their definitions are written in MySQL syntax, so `COPY FROM DATABASE` can fail on them. If it does, use Option 2.

---

## Option 2: copy only the 16 tables (more reliable)

A bash loop builds one `CREATE TABLE ... AS SELECT` for each table and sends all 16 to DuckDB in a single command:

```bash
duckdb sakila.duckdb -c "INSTALL mysql; LOAD mysql; ATTACH 'host=127.0.0.1 port=3306 user=root password=YOURPASS database=sakila' AS src (TYPE mysql, READ_ONLY); $(for t in actor address category city country customer film film_actor film_category film_text inventory language payment rental staff store; do echo "CREATE OR REPLACE TABLE $t AS SELECT * FROM src.$t;"; done)"
```

- `CREATE OR REPLACE` means you can run it again later without "table already exists" errors.
- The 16 tables are: actor, address, category, city, country, customer, film, film_actor, film_category, film_text, inventory, language, payment, rental, staff, store.

---

## Check the result

```bash
duckdb sakila.duckdb -c "SHOW TABLES; SELECT count(*) FROM rental;"
```

Expected: **16 tables**, and `rental` should have **16,044 rows**.

To count only base tables, not views:

```sql
SELECT count(*) FROM information_schema.tables WHERE table_type = 'BASE TABLE';  -- expect 16
```

---

## Notes

- `CREATE TABLE ... AS SELECT` copies columns and data but **not** primary or foreign keys. That's normal for analytics work, and in the dimensional modeling track you'll define your own keys anyway.
- You don't have to copy anything to practice: after the `ATTACH` you can query MySQL directly, for example `SELECT * FROM src.film;`. Copying is worth it once you want a single fast local file.
- **If Sakila is a SQLite file instead:** use `INSTALL sqlite; LOAD sqlite; ATTACH 'sqlite-sakila.db' AS src (TYPE sqlite);` and keep the rest the same.
