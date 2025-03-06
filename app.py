from main import classify_language
import gradio as gr

def interface():
    with gr.Blocks() as demo:
        gr.Markdown("""
        # 🌍 Language Classifier
        Enter a text snippet below, and we'll detect the language for you!
        """)
        
        textbox = gr.Textbox(lines=2, show_label=False, placeholder="Type your text here...")
        button = gr.Button("🔍 Classify", variant="primary")
        label = gr.Label()
        
        gr.Markdown("""
        - English: `1`
        - Thai: `2`
        - Other: `0`
        """)
        
        button.click(classify_language, inputs=textbox, outputs=label)
    
    return demo

demo = interface()
demo.launch()