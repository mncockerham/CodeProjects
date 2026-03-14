# DBeaver & DuckDB: Querying Iceberg Tables

Since DBeaver is your primary SQL IDE and already has a DuckDB connection configured, you can easily use it as a visual interface to query your local Apache Iceberg tables!

Because Iceberg is fundamentally a table format (metadata + parquet files) and *not* a running database server, we rely on DuckDB's powerful extensions to act as the query engine inside DBeaver.

Here is the step-by-step process to set this up.

## 1. Ensure the `iceberg` Extension is Installed in DuckDB
Before DBeaver can read the Iceberg metadata, the DuckDB engine needs the `iceberg` extension. 

Open a new SQL script in DBeaver connected to your DuckDB database and run:
```sql
INSTALL iceberg;
LOAD iceberg;
```
*(Note: You only need to run `INSTALL` once per machine, but `LOAD` might need to be run at the start of your DBeaver session depending on your DuckDB initialization settings).*

## 2. Querying the Iceberg Table
DuckDB allows you to query the Iceberg table *directly* by pointing it at the metadata JSON file or the root directory of the Iceberg table in your local warehouse.

### Option A: Querying the Directory (Easiest)
If you know the path to your Iceberg table (e.g., the `warehouse/local_schema.db/sample_users` path we created), you can query it using the `iceberg_scan` function:

```sql
SELECT * 
FROM iceberg_scan('/Users/mark/LocalData/Iceberg/warehouse/local_schema/sample_users');
```

Tip: You can use standard SQL aggregations, filtering, and joins right from this function!
```sql
SELECT status, COUNT(*), SUM(account_balance)
FROM iceberg_scan('/Users/mark/LocalData/Iceberg/warehouse/local_schema/sample_users')
GROUP BY status;
```

### Option B: Querying a Specific Metadata or Parquet File
For debugging or time-travel queries, you might want to point DuckDB exactly at an underlying metadata file or a specific parquet file inside the Iceberg data folder, using standard DuckDB functions:

```sql
-- Read raw parquet files directly (bypassing Iceberg metadata entirely)
SELECT * FROM read_parquet('/Users/mark/LocalData/Iceberg/warehouse/local_schema/sample_users/data/*.parquet');
```

## 3. Creating a View in DBeaver (Highly Recommended)
Constantly typing the full file path is tedious. The best practice when using DBeaver with DuckDB local files is to create a **View**. This makes the Iceberg table look and behave exactly like a native table in the DBeaver side panel structure.

Run this once:
```sql
CREATE OR REPLACE VIEW db_sample_users AS 
SELECT * FROM iceberg_scan('/Users/mark/LocalData/Iceberg/warehouse/local_schema/sample_users');
```

Now, in your DBeaver Database Navigator panel on the left, you can seamlessly expand `Views` -> `db_sample_users`, see the columns, and simply write:
```sql
SELECT * FROM db_sample_users LIMIT 10;
```

## Summary
By using `LOAD iceberg;` and the `iceberg_scan()` function wrapped in a SQL `VIEW`, DBeaver transforms into a fully-fledged Apache Iceberg IDE powered by the speed of DuckDB!
