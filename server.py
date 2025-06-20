from flask import Flask, render_template, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_prompt = request.form.get("prompt")

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openchat/openchat-7b",
            "messages": [
                {"role": "system", "content": "You are a ghost AI. Reply with creepy tone, short eerie sentences. Sometimes whisper, chuckle, or giggle. Always sound unsettling."},
                {"role": "user", "content": user_prompt}
            ]
        }

        try:
            res = requests.post(OPENROUTER_URL, headers=headers, json=payload)
            if res.status_code == 200:
                reply = res.json()["choices"][0]["message"]["content"]
                return reply
            else:
                return f"👻 Error from API: {res.status_code} – {res.text}"
        except Exception as e:
            return f"👻 The ghost encountered an error.\n{str(e)}"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")

