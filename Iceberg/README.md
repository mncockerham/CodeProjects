# Local Apache Iceberg Integration

This repository houses code explaining how to integrate, create, and query **Apache Iceberg** tables entirely locally, simulating a scalable data application architecture.

## Overview & Architecture

We have specifically designed this setup to physically separate your logic (code) from your structured data files:

1.  **Source Code & Version Control:** Lives here (`~/github/CodeProjects/Iceberg`). This directory is safely versioned in Git without the risk of checking in massive database or parquet files.
2.  **Catalog & Warehouse (The Data):** All database generation and actual `.parquet` file storage physically occur outside of this repo in `~/LocalData/Iceberg`.
    *   *Why?* It prevents iCloud sync collisions, isolates environments, and mimics how code interacts with a remote S3 bucket + Glue database in the cloud.

## Getting Started

### 1. Requirements

Ensure you have your environment set up with PyIceberg (using DuckDB and SQLite adapters installed natively). It is highly recommended to use a virtual environment.

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate it (Mac/Linux)
source .venv/bin/activate

# Install the dependencies
pip install -r requirements.txt
```

### 2. File Overview

*   **`create_sample_table.py`:** Initializes the external Iceberg directory, sets up an SQLite catalog to mimic the Iceberg rest catalog/glue, and appends a randomly generated 100-row PyArrow DataFrame into it using DuckDB.
*   **`query_table.py`:** Connects to your previously defined table, unpacks its metadata to see how Iceberg is managing the snapshots, and demonstrates using DuckDB directly against an active Iceberg dataset.

### 3. Usage

Run the scripts in sequence:

```bash
python create_sample_table.py
python query_table.py
```

### 4. Storage Under the Hood
After running the generation script, you can inspect the data directory on your Mac locally. This helps illustrate how Iceberg builds schemas dynamically.
*   **Catalog DB:** `~/LocalData/Iceberg/catalog/iceberg_catalog.db` - SQLite database storing table states and UUID mappings.
*   **Warehouse:** `~/LocalData/Iceberg/warehouse/local_schema.db/sample_users/` - Where the physical `.parquet` formats live alongside `.json`/`.avro` metadata describing table history.
