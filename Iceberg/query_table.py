import os
import pyarrow as pa
import duckdb
from pyiceberg.catalog.sql import SqlCatalog

# 1. Re-initialize Dynamic Paths
HOME = os.path.expanduser("~")
ICEBERG_DATA_DIR = os.path.join(HOME, "LocalData", "Iceberg")
CATALOG_DB_PATH = os.path.join(ICEBERG_DATA_DIR, "catalog", "iceberg_catalog.db")
WAREHOUSE_PATH = os.path.join(ICEBERG_DATA_DIR, "warehouse")

print(f"📁 Opening Catalog DB: {CATALOG_DB_PATH}")

# 2. Open the SQL Catalog
catalog = SqlCatalog(
    "default",
    **{
        "uri": f"sqlite:///{CATALOG_DB_PATH}",
        "warehouse": f"file://{WAREHOUSE_PATH}",
    }
)

namespace = "local_schema"
table_id = f"{namespace}.sample_users"

# 3. Load the Iceberg Table Object
print(f"📖 Loading table: {table_id}...")
table = catalog.load_table(table_id)

# 4. Extract data down to PyArrow
print("⏳ Scanning Iceberg table and converting to PyArrow...")
arrow_table = table.scan().to_arrow()

# 5. Connect to DuckDB natively
con = duckdb.connect()

print("\n" + "="*60)
print("🦆 DuckDB Query Results (Top 5 Inactive Users by Balance):")
print("="*60)

# DuckDB can natively query a variable named 'arrow_table' inside the python environment
result = con.execute("""
    SELECT 
        id, 
        username, 
        account_balance
    FROM arrow_table 
    WHERE status = 'Inactive' 
    ORDER BY account_balance DESC 
    LIMIT 5
""").fetchall()

for row in result:
    print(row)

# Bonus: Querying Metadata
print("\n" + "="*50)
print("📊 Iceberg Table Metadata")
print("="*50)
metadata = table.metadata
print(f"Format Version: {metadata.format_version}")
print(f"Last Updated:   {metadata.last_updated_ms}")
print(f"Total Snapshots: {len(metadata.snapshots)}")
print("="*50)
