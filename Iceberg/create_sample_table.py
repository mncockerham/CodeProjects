import os
import pyarrow as pa
import duckdb
from pyiceberg.catalog.sql import SqlCatalog
from pyiceberg.exceptions import NoSuchTableError

# 1. Define Paths Dynamically
# Use a non-synced folder under the user's home directory.
HOME = os.path.expanduser("~")
ICEBERG_DATA_DIR = os.path.join(HOME, "LocalData", "Iceberg")
CATALOG_DB_PATH = os.path.join(ICEBERG_DATA_DIR, "catalog", "iceberg_catalog.db")
WAREHOUSE_PATH = os.path.join(ICEBERG_DATA_DIR, "warehouse")

# 2. Ensure directories exist
os.makedirs(os.path.dirname(CATALOG_DB_PATH), exist_ok=True)
os.makedirs(WAREHOUSE_PATH, exist_ok=True)

print(f"📁 Using Catalog DB: {CATALOG_DB_PATH}")
print(f"📁 Using Warehouse: {WAREHOUSE_PATH}")

# 3. Initialize the SQL Catalog (SQLite backend)
catalog = SqlCatalog(
    "default",
    **{
        "uri": f"sqlite:///{CATALOG_DB_PATH}",
        "warehouse": f"file://{WAREHOUSE_PATH}",
    }
)

# 4. Create a namespace (schema like in a traditional database)
namespace = "local_schema"
catalog.create_namespace_if_not_exists(namespace)

# 5. Generate ~100 rows of sample data using DuckDB
print("\n⚙️  Generating sample data...")
con = duckdb.connect()

# Create a sample DataFrame and convert natively to a PyArrow Table
arrow_df = con.execute("""
    SELECT 
        id,
        'User_' || id AS username,
        CASE WHEN id % 2 = 0 THEN 'Active' ELSE 'Inactive' END AS status,
        round(random() * 1000, 2) AS account_balance
    FROM range(1, 101) series(id)
""").to_arrow_table()

# Define the table identifier
table_id = f"{namespace}.sample_users"

# 6. Clean up previous runs if the table already exists
try:
    catalog.drop_table(table_id)
    print(f"🗑️  Dropped existing table: {table_id}")
except NoSuchTableError:
    pass

# 7. Create the Iceberg Table
print(f"\n🧊 Creating Iceberg table: {table_id}")
table = catalog.create_table(
    identifier=table_id,
    schema=arrow_df.schema,
)

# 8. Append the sample data
print("✍️  Appending 100 rows to the table...")
table.append(arrow_df)

print(f"\n✅ Successfully wrote {len(arrow_df)} rows to local Iceberg table.")
print(f"📍 Iceberg Metadata Location: {table.location()}")
