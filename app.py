import os
import pickle

import numpy as np
import PyPDF2
from flask import Flask, jsonify, redirect, render_template, request


def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


def search_pdf(query, pdf_sentences):
    query_lower = query.lower()
    for sentence in pdf_sentences:
        if query_lower in sentence.lower():
            return sentence.strip()
    return "I don't understand 😅"


def safe_load_pickle(path):
    try:
        with open(path, "rb") as file:
            return pickle.load(file)
    except Exception as exc:
        print(f"Error loading {path}: {exc}")
        return None


def build_response(user, data_db, model_obj, vectorizer_obj, pdf_sentence_list):
    if user in ["hi", "hello", "hey"]:
        return "Hello 👋 I am Vedastra AI!"

    best_match = None
    for key in data_db:
        if key == user:
            best_match = key
            break
        if key in user:
            best_match = key

    if best_match:
        return data_db[best_match]

    if model_obj is not None and vectorizer_obj is not None:
        try:
            X = vectorizer_obj.transform([user])
            if hasattr(model_obj, "predict_proba"):
                probs = model_obj.predict_proba(X)
                confidence = float(np.max(probs))
                if confidence > 0.6:
                    return model_obj.predict(X)[0]
            else:
                return model_obj.predict(X)[0]
        except Exception as exc:
            print(f"Model inference failed: {exc}")

    return search_pdf(user, pdf_sentence_list)


model = safe_load_pickle("model.pkl")
vectorizer = safe_load_pickle("vectorizer.pkl")

pdf_file = "UPSC_Wallah_Books_Environment_and_Ecology.pdf"
if os.path.exists(pdf_file):
    try:
        pdf_text = read_pdf(pdf_file)
        pdf_sentences = [line.strip() for line in pdf_text.split(".") if line.strip()]
    except Exception as exc:
        print(f"Error loading PDF: {exc}")
        pdf_sentences = []
else:
    print(f"PDF file not found: {pdf_file}")
    pdf_sentences = []

API_KEY = os.getenv("VEDASTRA_API_KEY", "vedastra123")

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.txt")
CHAT_FILE = os.path.join(BASE_DIR, "chat.txt")


def load_data():
    data = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(":", 1)
                if len(parts) == 2:
                    data[parts[0].strip().lower()] = parts[1].strip()
    return data


def load_chat():
    history = []
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r", encoding="utf-8") as file:
            for line in file:
                if "||" in line:
                    sender, message = line.strip().split("||", 1)
                    history.append((sender, message))
    return history


def save_chat(sender, message):
    with open(CHAT_FILE, "a", encoding="utf-8") as file:
        file.write(f"{sender}||{message}\n")


chat_history = load_chat()


@app.route("/", methods=["GET", "POST"])
def home():
    global chat_history
    data_db = load_data()

    if request.method == "POST":
        user = request.form.get("question", "").strip().lower()
        response = build_response(user, data_db, model, vectorizer, pdf_sentences)

        chat_history.append(("user", user))
        save_chat("user", user)
        chat_history.append(("ai", response))
        save_chat("ai", response)

        return redirect("/")

    return render_template("index.html", chat_history=chat_history)


@app.route("/api/chat", methods=["POST"])
def api_chat():
    api_key = request.args.get("api_key")
    if api_key != API_KEY:
        return jsonify({"error": "Unauthorized ❌"}), 401

    payload = request.get_json(silent=True) or {}
    user = payload.get("message", "").strip().lower()

    data_db = load_data()
    response = build_response(user, data_db, model, vectorizer, pdf_sentences)

    return jsonify({"user": user, "response": response})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)