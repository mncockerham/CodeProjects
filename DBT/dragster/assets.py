from dagster import asset
import pandas as pd
from sqlalchemy import create_engine
import duckdb

# 1. Extract from Postgres (E)
@asset
def raw_airport_data() -> pd.DataFrame:
    """Extracts the airport table from Postgres into a Pandas DataFrame."""
    # Connect to the local Postgres instance
    # Notice we don't use a password here because we removed it earlier
    engine = create_engine('postgresql://postgres@localhost:5432/postgres_air')
    
    # Read the data straight into memory. Dagster will automatically serialize this output
    # to your local drive behind the scenes so the next asset can use it!
    df = pd.read_sql("SELECT * FROM postgres_air.airport", con=engine)
    return df

# 2. Load into DuckDB (L)
@asset
def duckdb_airport_table(raw_airport_data: pd.DataFrame):
    """Takes the extracted Pandas DataFrame and loads it into our DuckDB data warehouse."""
    # Connect to our local dbt DuckDB file
    con = duckdb.connect('/Users/mark/github/CodeProjects/DBT/local.duckdb')
    
    import pyarrow as pa
    
    # DuckDB sometimes struggles with Pandas 3.0 string types in memory. 
    # Converting it to a PyArrow table explicitly prevents this!
    arrow_table = pa.Table.from_pandas(raw_airport_data)
    con.register("arrow_airport_data", arrow_table)
    con.execute("CREATE OR REPLACE TABLE raw_airport AS SELECT * FROM arrow_airport_data")
    
    con.close()
