from query_agent import promo_query_agent
from intent_analyzer_agent import promo_intent_analyzer_agent

def process_query(query):
    """Process user query by analyzing intent and querying data."""
    try:
        intent_response = promo_intent_analyzer_agent(query)
        query_response = promo_query_agent(intent_response)
        return query_response
    except Exception as e:
        return f"Error: {str(e)}"
    
if __name__ == "__main__":
    print("Query Agent (Type 'q' to quit)")
    while True:
        query = input("Enter text: ")
        if query.lower() == "q":
            print("Goodbye!")
            break
        response = process_query(query)
        print(response)