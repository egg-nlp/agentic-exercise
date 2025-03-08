import os
import duckdb
from dotenv import load_dotenv
from openai import OpenAI
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

system_prompt = f"""
You are the query agent.
You must figure out the SQL query to prepare data to answer the question. Therefore, return only the answer and do not include prefixes, suffixes, or prologues. 
Ensure that your SQL answer is runnable on DuckDB.
Current date: {current_date}
If the user's query is not related to the table, provide a brief response related to the user's query.
"""

def promo_query_agent(query: str):
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