# Connecting Superset to Your Data Stack

Apache Superset supports connecting to a wide array of SQL-speaking databases via SQLAlchemy dialects. Because you are using a local ecosystem with PostgreSQL, DuckDB, and Apache Iceberg, this guide outlines the specific setup and best practices for configuring these sources.

---

## 🐘 1. Connecting to PostgreSQL

PostgreSQL is natively supported by Superset and is one of the most common data sources. Since your Dagster project (`dagster_postgres_air`) already utilizes PostgreSQL, this is typically the first and most stable connection to configure.

### Setup Instructions
1.  **Ensure Driver is Installed:** Superset's standard Docker image already includes the `psycopg2` driver. You usually do not need to install anything extra.
2.  **Add Database:** In the Superset UI, go to **Settings (Gear Icon) -> Database Connections -> + Database**.
3.  **Connection URI:** Choose PostgreSQL and enter your SQLAlchemy URI. It will look like this:
    ```
    postgresql://<username>:<password>@<host>:<port>/<database_name>
    ```
    *   *If running Superset via Docker and Postgres locally on your Mac:* You cannot use `localhost` because that refers to the inside of the Superset container. Instead, use `host.docker.internal` as the `<host>`.
4.  **Test & Save:** Click "Test Connection" and then save it. Your tables will now be available for creating Datasets.

---

## 🦆 2. Connecting to DuckDB

Superset does not have a native, built-in dropdown for DuckDB out-of-the-box, but it connects seamlessly via the `duckdb-engine` SQLAlchemy driver.

### Setup Instructions
1.  **Install the Driver:** If you are running Superset in Docker, you must add the Python driver to the image. This requires either creating a custom `Dockerfile` or running this inside the container:
    ```bash
    pip install duckdb-engine
    ```
2.  **Add Database:** Go to **Database Connections -> + Database**. Select **Other** (or Supported Databases dropdown empty search) using a custom SQLAlchemy URI.
3.  **Connection URI:**
    ```
    duckdb:////path/to/your/database.duckdb
    ```
    *   *Important:* If Superset is in Docker, the `/path/to/your/...` must be *mounted* inside the docker container using docker-compose volumes. Superset cannot read arbitrary files on your Mac's hard drive without permission.
    *   *In-Memory:* If you just want an empty temporary database, use `duckdb:///:memory:`

---

## 🧊 3. Querying Apache Iceberg Tables (The Best Way)

Superset currently queries databases, not raw file formats. To query Iceberg tables in Superset, you need a compute engine sitting between Superset and the Parquet files.

While you *could* use heavy engines like Trino or Dremio, **the absolute best way for local development is to use DuckDB as the engine.**

### The Process
You will connect Superset to DuckDB (following the steps in section 2), and then instruct DuckDB to query your Iceberg tables.

1.  **Mount the Warehouse:** Ensure your `~/LocalData/Iceberg` directory is mounted via a docker-compose volume into the Superset container (e.g., mapped to `/app/iceberg_data`).
2.  **Ensure Extensions:** DuckDB inside the container needs the `iceberg` extension. 
3.  **Create Views via the SQL Lab:**
    Once DuckDB is connected in Superset, open Superset's **SQL Lab** and run queries using DuckDB's Iceberg extension:
    
    ```sql
    -- Load the extension (if not already loaded globally)
    INSTALL iceberg;
    LOAD iceberg;
    
    -- Query the table directory directly!
    SELECT * FROM iceberg_scan('/app/iceberg_data/warehouse/local_schema/sample_users');
    ```
4.  **Create a Virtual Dataset:**
    Instead of typing `iceberg_scan` every time you build a dashboard, run your `SELECT * FROM iceberg_scan(...)` query in SQL Lab, and simply click **"Save Dataset"**.
    
    Superset will save this as a "Virtual Dataset". You can then build all your charts and dashboards on top of this Virtual Dataset exactly as if it were a physical PostgreSQL table!

### Advantages of this Approach
*   **Zero Infrastructure:** No need to spin up a giant Trino cluster or an AWS Athena instance just to visualize local Iceberg files.
*   **Blazing Fast:** DuckDB's vectorized execution engine processes the Iceberg parquet files incredibly quickly.
*   **Logical Abstraction:** The Superset "Virtual Dataset" completely abstracts the messy file paths away from the end-user building the dashboard.
