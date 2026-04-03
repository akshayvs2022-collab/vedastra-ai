from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.txt")

def load_data():
    data = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    data[parts[0].lower()] = parts[1]
    return data

chat_history = []   # 🔥 store conversation

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
                response = "I don't understand 😅"

        chat_history.append(("user", user))
        chat_history.append(("ai", response))

        return redirect("/")   # ✅ correct indent

    return render_template("index.html", chat_history=chat_history)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)