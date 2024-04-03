from flask import Flask

app = Flask(__name__)

@app.route("/")
def frontPage():
    return "<p>Hello, World!</p>"


