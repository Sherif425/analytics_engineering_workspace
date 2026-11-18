# Loading Sakila DB into DuckDB

## 1. Loading from SQLite File

You can load and query a Sakila SQLite database (`sakila.db`) in DuckDB using the built-in SQLite extension.

### Method 1: Query SQLite Directly (Attach)
DuckDB can attach and query a SQLite file directly without copying all the data into a native DuckDB file:

```sql
-- 1. Install and load the SQLite extension (only needed once)
INSTALL sqlite;
LOAD sqlite;

-- 2. Attach the Sakila SQLite database
ATTACH 'sakila.db' AS sakila (TYPE sqlite);

-- 3. Query the attached tables
USE sakila;
SHOW TABLES;
SELECT title, release_year, length FROM sakila.film LIMIT 5;
```

### Method 2: Copy SQLite Tables into a Native DuckDB Database
If you want to permanently copy and store the Sakila tables into a native DuckDB database file, you can attach the SQLite file and copy the tables over:

```sql
-- 1. Create and connect to a new DuckDB database file
ATTACH 'sakila.duckdb' AS new_db;

-- 2. Install and attach the SQLite database
INSTALL sqlite;
LOAD sqlite;
ATTACH 'sakila.db' AS sakila_sqlite (TYPE sqlite);

-- 3. Copy tables into DuckDB (example: film table)
CREATE TABLE new_db.film AS SELECT * FROM sakila_sqlite.film;
```

### Method 3: Using Python
You can also automate the loading process using Python and the `duckdb` library:

```python
import duckdb

# Connect to a new or existing DuckDB file
con = duckdb.connect("sakila.duckdb")

# Install and load the sqlite extension
con.execute("INSTALL sqlite;")
con.execute("LOAD sqlite;")

# Attach the SQLite database
con.execute("ATTACH 'sakila.db' AS sakila (TYPE sqlite);")

# Copy a table into DuckDB
con.execute("CREATE TABLE film AS SELECT * FROM sakila.film;")
```

---

## 2. Connecting to MySQL and Loading Sakila Tables

DuckDB can connect directly to a running MySQL instance and load the Sakila tables using the official DuckDB MySQL Extension. DuckDB uses a PostgreSQL-style key=value configuration format to `ATTACH` the database.

### Step 1: Install and Connect (SQL)
Run this inside your DuckDB CLI or query environment to link your MySQL database:

```sql
-- 1. Install and load the MySQL extension
INSTALL mysql;
LOAD mysql;

-- 2. Attach your MySQL database (Replace with your actual credentials/host)
ATTACH 'host=localhost user=dbadmin password=p@SS0987vcx port=3306 database=sakila' 
    AS mysql_sakila (TYPE mysql);

-- 3. Switch context to the MySQL instance to verify tables
USE mysql_sakila;
SHOW TABLES;
```

### Step 2: Ingest the Data into DuckDB
Because DuckDB reads data from MySQL on the fly during a query, it is highly recommended to clone the tables locally into native DuckDB storage to boost performance:

```sql
-- Create local copies of tables inside DuckDB
CREATE TABLE local_film AS SELECT * FROM mysql_sakila.film;
CREATE TABLE local_actor AS SELECT * FROM mysql_sakila.actor;
```

```sql
SELECT 'CREATE TABLE ' || table_name || ' AS SELECT * FROM mysql_db.' || table_name || ';' 
FROM information_schema.tables 
WHERE table_schema = 'mysql_sakila';
```
### Alternative: Using Python
If you prefer managing this via a Python script, you can initialize the connection block programmatically:

```python
import duckdb

# Connect to a native DuckDB file
con = duckdb.connect("my_local_sakila.duckdb")

# Setup the MySQL extension
con.execute("INSTALL mysql;")
con.execute("LOAD mysql;")

# Connect to the remote or local MySQL instance
con.execute("""
    ATTACH 'host=127.0.0.1 user=root password=secret port=3306 database=sakila' 
    AS mysql_db (TYPE mysql);
""")

# Example query pulling live from MySQL into a Python DataFrame
df = con.execute("SELECT * FROM mysql_db.film LIMIT 5;").df()
print(df)
```