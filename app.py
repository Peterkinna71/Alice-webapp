from flask import Flask, request, jsonify, render_template
import openai
import requests
import os

app = Flask(__name__)

# OpenAI och ElevenLabs API-nycklar
openai.api_key = "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"
ELEVENLABS_API_KEY = "sk_14d7d3390225c54b4f8714c962e5a40fcc32f16a0d492e0f"
VOICE_ID = "gyxv2BmRSTkWWyWlpbcJ"

# Textgenerering med OpenAI
def generate_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Du är Alice, en glad och lite flörtig AI-assistent."},
            {"role": "user", "content": user_input}
        ]
    )
    return response['choices'][0]['message']['content']

# Text till tal med ElevenLabs
def text_to_speech(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.7, "similarity_boost": 0.8}
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        audio_path = "static/audio/alice_response.mp3"
        with open(audio_path, "wb") as audio_file:
            audio_file.write(response.content)
        return "alice_response.mp3"
    else:
        return None

# Startsida
@app.route('/')
def home():
    return render_template('index.html')

# API-endpoint för att fråga Alice
@app.route('/ask_alice', methods=['POST'])
def ask_alice():
    data = request.json
    if not data or 'question' not in data:
        return jsonify({"error": "Ingen fråga skickades."}), 400

    question = data['question']
    response = generate_response(question)
    audio_file = text_to_speech(response)

    return jsonify({
        "response": response,
        "audio_file": audio_file
    })

if __name__ == '__main__':
    # Skapa mappen för ljudfiler om den inte finns
    if not os.path.exists("static/audio"):
        os.makedirs("static/audio")

    app.run(debug=True)
