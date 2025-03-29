import os
import json
from flask import Flask, request, jsonify
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)

# Check if API key is available
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable is missing. Please set it before running the server.")

# Configure the generative AI model
genai.configure(api_key=api_key)

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

try:
    model = genai.GenerativeModel(
        model_name="tunedModels/tasnimdisha-sp48u93mq7rt",
        generation_config=generation_config,
    )

    # Start chat session with predefined history
    chat_session = model.start_chat(
        history=[
            {"role": "user", "parts": ["Hi there, what are you doing today?"]},
            {"role": "model", "parts": ["I'm working on improving my SEO and content marketing skills."]},
            {"role": "user", "parts": ["What is your name?"]},
            {"role": "model", "parts": ["My name is Tasnim Disha. I'm a digital marketer and SEO expert."]},
        ]
    )
except Exception as e:
    raise RuntimeError(f"Error initializing generative AI model: {e}")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Validate JSON request
        if not request.is_json:
            return jsonify({'error': 'Invalid request format. Expected JSON.'}), 400

        data = request.get_json()
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400

        # Send the message to the chat session
        response = chat_session.send_message(user_message)

        if not response or not response.text:
            return jsonify({'error': 'No response from AI model'}), 500

        return jsonify({'response': response.text})

    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON format'}), 400
    except Exception as e:
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
