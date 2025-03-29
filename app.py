import os
import json
from flask import Flask, request, jsonify
import google.generativeai as genai

# Configure the generative AI model with your API key
genai.configure(api_key=os.environ["AIzaSyCtF36sFCcJe3EkVwHc_Olin4TE43Bee9Q"])

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="tunedModels/tasnimdisha-sp48u93mq7rt",
    generation_config=generation_config,
)

# Initialize Flask app
app = Flask(__name__)

# Starting a chat session with initial history
chat_session = model.start_chat(
    history=[
        {"role": "user", "parts": ["Hi there, what are you doing today?"]},
        {"role": "model", "parts": ["I'm working on improving my SEO and content marketing skills."]},
        {"role": "user", "parts": ["What is your name?"]},
        {"role": "model", "parts": ["My name is Tasnim Disha. I'm a digital marketer and SEO expert."]},
        # Add more sample messages if needed
    ]
)

@app.route('/chat', methods=['POST'])
def chat():
    # Get user message from request
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Send the message to the chat session
    response = chat_session.send_message(user_message)

    # Return the bot's response as JSON
    return jsonify({'response': response.text})

if __name__ == '__main__':
    app.run(debug=True)
