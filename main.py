import os
from openai import OpenAI
from dotenv import load_dotenv
from prompt import system_prompt

load_dotenv()

TYPHOON_API_KEY = os.getenv("TYPHOON_API_KEY")

llm = OpenAI(
   api_key=TYPHOON_API_KEY,
   base_url='https://api.opentyphoon.ai/v1'
)

def classify_language(user_input):
    response = llm.chat.completions.create(
        model="typhoon-v2-70b-instruct",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    return response.choices[0].message.content.strip()

print("Language Classifier (Type 'q' to quit)")
print("English: 1, Thai: 2, Other: 0")
while True:
    user_input = input("Enter text: ")
    if user_input.lower() == "q":
        print("Goodbye!")
        break
    response = classify_language(user_input)
    print(int(response))