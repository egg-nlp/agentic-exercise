import os
from retry import retry
from openai import OpenAI
from dotenv import load_dotenv
from prompt import system_prompt

load_dotenv()

TYPHOON_API_KEY = os.getenv("TYPHOON_API_KEY")

llm = OpenAI(
   api_key=TYPHOON_API_KEY,
   base_url='https://api.opentyphoon.ai/v1'
)

@retry(ValueError, tries=3, delay=2, backoff=2)
def classify_language(user_input: str) -> str:
    response = llm.chat.completions.create(
        model="typhoon-v2-70b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
    )

    response = int(response.choices[0].message.content.strip())
    match response:
        case 1:
            return "English"
        case 2:
            return "Thai"
        case 0:
            return "Other"
        case _:
            return ValueError("Out of bound")

if __name__ == "__main__":
    print("Language Classifier (Type 'q' to quit)")

    while True:
        user_input = input("Enter text: ")
        if user_input.lower() == "q":
            print("Goodbye!")
            break
        response = classify_language(user_input)
        print(response)