import pickle

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
API_KEY = "vedastra123"   # 🔐 your secret key
from flask import Flask, render_template, request, redirect, jsonify
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.txt")
CHAT_FILE = os.path.join(BASE_DIR, "chat.txt")   # 🔥 new

# Load AI data
def load_data():
    data = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    data[parts[0].lower()] = parts[1]
    return data

# 🔥 Load chat history from file
def load_chat():
    history = []
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r", encoding="utf-8") as file:
            for line in file:
                if "||" in line:
                    sender, message = line.strip().split("||", 1)
                    history.append((sender, message))
    return history

# 🔥 Save chat to file
def save_chat(sender, message):
    with open(CHAT_FILE, "a", encoding="utf-8") as file:
        file.write(f"{sender}||{message}\n")

# 🔥 load existing chat
chat_history = load_chat()
@app.route("/", methods=["GET", "POST"])
def home():
    global chat_history
    data = load_data()

    if request.method == "POST":
        user = request.form.get("question", "").lower()

        if user in ["hi", "hello", "hey"]:
            response = "Hello 👋 I am Vedastra AI!"
        else:
            best_match = None

            for key in data:
                if key == user:
                    best_match = key
                    break
                elif key in user:
                    best_match = key

            if best_match:
                response = data[best_match]
            else:
    X = vectorizer.transform([user])
    response = model.predict(X)[0]

        chat_history.append(("user", user))
        save_chat("user", user)

        chat_history.append(("ai", response))
        save_chat("ai", response)

        return redirect("/")

    return render_template("index.html", chat_history=chat_history)
@app.route("/api/chat", methods=["POST"])
def api_chat():
    api_key = request.args.get("api_key")

    # 🔐 check key
    if api_key != API_KEY:
        return jsonify({
            "error": "Unauthorized ❌"
        }), 401

    data = request.json
    user = data.get("message", "").lower()

    data_db = load_data()

    if user in ["hi", "hello", "hey"]:
        response = "Hello 👋 I am Vedastra AI!"
    else:
        best_match = None

        for key in data_db:
            if key == user:
                best_match = key
                break
            elif key in user:
                best_match = key

        if best_match:
            response = data_db[best_match]
        else:
            response = "I don't understand 😅"

    return jsonify({
        "user": user,
        "response": response
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)