import os
import duckdb
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import pytz

load_dotenv()

TYPHOON_API_KEY = os.getenv("TYPHOON_API_KEY")

llm = OpenAI(
    api_key=TYPHOON_API_KEY,
    base_url='https://api.opentyphoon.ai/v1'
)

tz_utc7 = pytz.timezone('Asia/Bangkok')
now = datetime.now()
current_date = now.strftime("%A, %B %d, %Y")

# Load the dataset
df = pd.read_csv("../data/promo_studio_example_data.csv")
dic_df = pd.read_csv("../data/promo_studio_data_dictionary.csv")
duckdb.sql("CREATE TABLE dataset_table AS SELECT * FROM df")
duckdb.sql("INSERT INTO dataset_table SELECT * FROM df")
duckdb.sql("CREATE TABLE data_dic_table AS SELECT * FROM dic_df")
duckdb.sql("INSERT INTO data_dic_table  SELECT * FROM dic_df")
describe = duckdb.sql("DESCRIBE dataset_table").to_df()[["column_name", "column_type"]].to_string(max_rows=100)
data_dic = duckdb.sql("SELECT * FROM data_dic_table").to_df().to_string()

system_prompt=f"""
You are the query agent. You have access to a dataset with the following table name: dataset_table,\n\n
Columns:\n\n
{describe}\n\n
Data Dictionary:\n\n
{data_dic}\n\n
Current date: {current_date}\n\n
You must figure out the SQL query to prepare data to answer the question. Therefore, return any the answer and not include prefixes, suffixed and prologues Also, you must ensure that your SQL answer is runable on DuckDB"""

def promo_query_agent(query: str) -> pd.DataFrame:
    response = llm.chat.completions.create(
        model="typhoon-v2-70b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],

    )

    response = response.choices[0].message.content.strip()
    sql_keywords = ["SELECT", "WITH", "INSERT", "UPDATE", "DELETE"]
    if any(response.upper().startswith(keyword) for keyword in sql_keywords):
        return duckdb.sql(response).to_df()
    else:
        return response

if __name__ == "__main__":
    print("Query Agent (Type 'q' to quit)")

    while True:
        query = input("Enter text: ")
        if query.lower() == "q":
            print("Goodbye!")
            break
        response = promo_query_agent(query)
        print(response)