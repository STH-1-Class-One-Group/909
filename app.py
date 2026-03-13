
import sqlite3
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS 
 

app = Flask(__name__)
CORS(app)

app.json.ensure_ascii = False

conn = sqlite3.connect("practic.db")
cur = conn.cursor()

cur.execute("""
            CREATE TABLE IF NOT EXISTS logs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT
            )
            """)

conn.commit()

conn.close()

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/get_test", methods=["GET"])
def get_test():
    return jsonify({
        "name":"self.response(909)",
        "team":["팀장님", "오른팔", "왼팔"]
    })

@app.route("/post_test", methods=["POST"])
def post_test():
    request_data = request.get_json()
    real_msg = request_data.get("msg")

    return jsonify({
        "message": f"{real_msg}"
    })
    
if __name__ == "__main__":
    app.run(debug=True, port=8000)