from flask import Flask, jsonify, render_template
from flask_cors import CORS



app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=8000)