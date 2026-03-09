from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index(): #index.html을 잇는
    return render_template('index.html')

@go_get.route('/go_get', method="GET") #GET 요청용
def GET_choose():
    return "GET 받음!!"


@post_choose.route('/') #POST 요청용
def POST_choose():
    return "POST 받음!!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


