import duckdb
con = duckdb.connect("playstore.duckdb")
print(con.execute("SHOW TABLES").fetchdf())
for table in con.execute("SHOW TABLES").fetchdf()["name"]:
    count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"{table}: {count} rows")
