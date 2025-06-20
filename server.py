import os
from flask import Flask, request, render_template
from flask_cors import CORS
from gtts import gTTS
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form.get("prompt", "")
        if not prompt:
            return "👻 No input received."

        try:
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": "You are a creepy ghost that whispers haunted replies in a spooky tone."},
                    {"role": "user", "content": prompt}
                ]
            }

            response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

            if response.status_code == 200:
                reply = response.json()["choices"][0]["message"]["content"]

                # Generate creepy voice audio
                tts = gTTS(reply, lang='en')
                tts.save("static/voice.mp3")

                return reply
            else:
                return f"👻 Error from API: {response.status_code} – {response.text}"

        except Exception as e:
            return f"👻 The ghost encountered an error: {str(e)}"

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

