import os
import requests
from flask import Flask, render_template, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route("/", methods=["GET", "POST"])
def index():
    reply = ""
    if request.method == "POST":
        prompt = request.form.get("prompt")

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are a creepy ghost. Answer with haunted tone and eerie vibes."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(GROQ_API_URL, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            reply = result["choices"][0]["message"]["content"]
        else:
            reply = f"👻 Error from API: {response.status_code} – {response.text}"

    return render_template("index.html", reply=reply)

