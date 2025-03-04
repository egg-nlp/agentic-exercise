import duckdb

df = duckdb.query("SELECT * FROM read_parquet('sample.dataset.parquet')")
print(df)