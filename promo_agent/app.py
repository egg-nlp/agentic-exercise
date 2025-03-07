import gradio as gr
from query_agent import promo_query_agent

def chat_interface(query, history):
    try:
        response = promo_query_agent(query)
        return str(response)
    except Exception as e:
        return f"Error: {str(e)}"

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    query_input = gr.Textbox(placeholder="Enter your query here...")
    submit_btn = gr.Button("Submit")
    
    def respond(message, history):
        history.append((message, chat_interface(message, history)))
        return history, ""
    
    submit_btn.click(respond, [query_input, chatbot], [chatbot, query_input])

demo.launch()