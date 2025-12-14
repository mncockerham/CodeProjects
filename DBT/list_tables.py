import duckdb
try:
    con = duckdb.connect()
    con.install_extension('postgres')
    con.load_extension('postgres')
    print("Attaching postgres_air...")
    con.sql("ATTACH 'postgresql://postgres:ZAQ!2wsx@localhost:5432/postgres_air' AS pg (TYPE POSTGRES, READ_ONLY)")
    print("Attached. Querying tables...")
    res = con.sql("DESCRIBE pg.postgres_air.phone").fetchall()
    print("Tables found:", res)
except Exception as e:
    print("Error:", e)
