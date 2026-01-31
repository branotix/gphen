from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello Railway 🚆 Flask is working!"

@app.route("/health")
def health():
    return "ok", 200

