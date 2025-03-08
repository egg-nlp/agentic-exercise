import duckdb
import pandas as pd

# Define tables
tables = ["promo_dataset", "promo_data_dic"]

data_dic = ""
describe = ""

# Load and process each table
for table in tables:
    df = pd.read_csv(f"../data/{table}.csv")
    duckdb.sql(f"CREATE TABLE {table} AS SELECT * FROM df")
    duckdb.sql(f"INSERT INTO {table} SELECT * FROM df")
    
    if "dic" in table:
        data_dic = f"{table} table:\n" + duckdb.sql(f"SELECT * FROM {table}").to_df().to_string()
    else:
        describe = f"{table} table:\n" + duckdb.sql(f"DESCRIBE {table}").to_df()[["column_name", "column_type"]].to_string(max_rows=100)