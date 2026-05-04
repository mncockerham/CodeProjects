import os
import pyarrow as pa
import duckdb
import lancedb

# 1. Define Paths Dynamically
# Use a non-synced folder under the user's home directory.
HOME = os.path.expanduser("~")
LANCE_DATA_DIR = os.path.join(HOME, "LocalData", "Lance")

# 2. Ensure directories exist
os.makedirs(LANCE_DATA_DIR, exist_ok=True)

print(f"📁 Using LanceDB Directory: {LANCE_DATA_DIR}")

# 3. Initialize the LanceDB Database
db = lancedb.connect(LANCE_DATA_DIR)

# 4. Generate ~100 rows of sample data using DuckDB
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

table_name = "sample_users"

# 5. Create the LanceDB Table and append data
print(f"\n🧊 Creating LanceDB table: {table_name}")
print("✍️  Writing 100 rows to the table...")

# LanceDB can create the table and insert the initial data in one step
table = db.create_table(table_name, data=arrow_df, mode="overwrite")

print(f"\n✅ Successfully wrote {len(arrow_df)} rows to local LanceDB table.")
print(f"📍 LanceDB Metadata Location: file://{os.path.join(LANCE_DATA_DIR, table_name + '.lance')}")
