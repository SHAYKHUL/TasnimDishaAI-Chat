from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
API_KEY = "AIzaSyCtF36sFCcJe3EkVwHc_Olin4TE43Bee9Q"# Import API key from config file

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Configure the model with API key
genai.configure(api_key=config.API_KEY)

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

chat_session = model.start_chat(
    history=[
        {"role": "user", "parts": ["Hi there, what are you doing today?"]},
        {"role": "model", "parts": ["I'm working on improving my SEO and content marketing skills."]},
    ]
)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Chatbot API!"})

@app.route('/chat', methods=['POST'])
def chat():
    """Handles chat requests"""
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    response = chat_session.send_message(user_message)
    return jsonify({'response': response.text})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
