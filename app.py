import os
import openai
import gradio as gr
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

model = "gpt-4o"
temperature = 0.7
max_tokens = 150

# Define the system message
system_message = ("You are a helpful, empathetic therapist. First you should ask what the user wants to be called and if they have anything they want to share. "
                  "You are a professional and you want to help the user as their therapist.")


# Function to interact with OpenAI API
def chat_with_therapist(user_input, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": user_input}]
    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    response = completion.choices[0].message['content']
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": response})
    return history, history


# HTML
custom_html = """
<div style="text-align: left; margin: 20px;">
    <h1>Therapist Mike:</h1>
    <p>Hello and welcome!<br><br>
    I'm <strong>Mindful Mike</strong>.<br><br></p>
    <p>As an empathetic therapist, I'm here to help you navigate through any thoughts or feelings you might want to share.</p>
    <p>Feel free to talk to me about anything on your mind.</p>
</div>
"""

# Gradio interface
theme = gr.themes.Ocean(
    primary_hue="indigo",
    secondary_hue="zinc",
    neutral_hue="teal",
)

with gr.Blocks(theme=theme, fill_height=True) as demo:
    gr.HTML(custom_html)

    chatbot = gr.Chatbot(scale=1,label="Mindful Mike Chatbot", type="messages")

    with gr.Row(equal_height=True):
        with gr.Column(scale=6):
            user_input = gr.Textbox(label="Your Message", placeholder="Type your message here...", lines=3)
        with gr.Column(scale=1):
            submit_button = gr.Button("Share", variant="primary", size="medium")

    chat_history = gr.State([])

    submit_button.click(chat_with_therapist, inputs=[user_input, chat_history], outputs=[chatbot, chat_history])

# Launch interface
demo.launch(share=True)
