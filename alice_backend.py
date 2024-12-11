import speech_recognition as sr
import openai
import requests
import os

# Speech to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Prata med Alice...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="sv-SE")
            print(f"Du sa: {text}")
            return text
        except sr.UnknownValueError:
            print("Jag kunde inte förstå dig. Kan du säga det igen?")
            return None
        except sr.RequestError:
            print("Problem med API:t. Försök igen.")
            return None

# Text generation
openai.api_key = "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"

def generate_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Du är Alice, en glad och lite flörtig AI-assistent."},
            {"role": "user", "content": user_input}
        ]
    )
    return response['choices'][0]['message']['content']

# Text to speech
def text_to_speech(text, voice_id="gyxv2BmRSTkWWyWlpbcJ"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": "sk_14d7d3390225c54b4f8714c962e5a40fcc32f16a0d492e0f"
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.7, "similarity_boost": 0.8}
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        with open("alice_response.mp3", "wb") as file:
            file.write(response.content)
        print("Alice svarade med en röstfil!")
        return "alice_response.mp3"
    else:
        print("Något gick fel med ElevenLabs API.")
        return None

# Main function
def backend_test():
    user_input = speech_to_text()
    if user_input:
        print(f"Du sa: {user_input}")
        response = generate_response(user_input)
        print(f"Alice svarar: {response}")
        audio_file = text_to_speech(response)
        if audio_file:
            os.system(f"start {audio_file}")  # Windows, använd 'afplay' för Mac
        else:
            print("Alice kunde inte prata just nu.")
    else:
        print("Ingen input registrerades.")

if __name__ == "__main__":
    backend_test()

