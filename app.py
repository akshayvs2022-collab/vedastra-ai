from flask import Flask, render_template, request
import os

app = Flask(__name__)

DATA_FILE = "data.txt"

# Load data
def load_data():
    data = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    data[parts[0].lower()] = parts[1]
    return data

@app.route("/", methods=["GET", "POST"])
def home():
    response = ""
    data = load_data()

    if request.method == "POST":
        user = request.form["question"].lower()

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

    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)