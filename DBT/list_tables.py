import duckdb
try:
    con = duckdb.connect()
    con.install_extension('postgres')
    con.load_extension('postgres')
    print("Attaching postgres_air...")
    con.sql("ATTACH 'postgresql://postgres:ZAQ!2wsx@localhost:5432/postgres_air' AS pg (TYPE POSTGRES, READ_ONLY)")
    print("Attached. Querying tables...")
    res = con.sql("SELECT table_schema, table_name FROM pg.information_schema.tables WHERE table_schema NOT IN ('information_schema', 'pg_catalog')").fetchall()
    print("Tables found:", res)
except Exception as e:
    print("Error:", e)
