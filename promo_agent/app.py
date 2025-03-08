import gradio as gr
from chain import process_query

def chat_interface(message, history):
    response = process_query(message)
    history.append((message, str(response)))
    return history, ""

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    query_input = gr.Textbox(placeholder="Enter your query here...")
    submit_btn = gr.Button("Submit")
    
    submit_btn.click(chat_interface, [query_input, chatbot], [chatbot, query_input])

demo.launch()