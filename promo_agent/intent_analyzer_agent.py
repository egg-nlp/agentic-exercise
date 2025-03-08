import os
from db import data_dic, describe
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
TYPHOON_API_KEY = os.getenv("TYPHOON_API_KEY")

llm = OpenAI(
    api_key=TYPHOON_API_KEY,
    base_url='https://api.opentyphoon.ai/v1'
)

system_prompt = f"""
You are an intent analyzer agent.
Your task is to analyze the intent of the user query and provide the following:
- Table Name
- Table Description
- Data Dictionary

Columns:

{describe}

Data Dictionary:

{data_dic}

Expected output:
- User Query
- Table Name
- Table Description
- Data Dictionary

If the user's query is not related to the table, return only the user's query.
"""

def promo_intent_analyzer_agent(query: str):
    response = llm.chat.completions.create(
        model="typhoon-v2-70b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    print("Query Agent (Type 'q' to quit)")
    while True:
        query = input("Enter text: ")
        if query.lower() == "q":
            print("Goodbye!")
            break
        response = promo_intent_analyzer_agent(query)
        print(response)