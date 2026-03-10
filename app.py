from flask import Flask, render_template, jsonify 
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index(): 
    return render_template('index.html') #index.html을 잇는

@app.route('/go_get', methods=["GET"]) #GET 요청용 , /go_get 저요!!!
def GET_choose():
    return jsonify({"m" : "get 받음!!"})


@app.route('/go_post', methods=["POST"]) #POST 요청용
def POST_choose():
    return jsonify({"m" : "post 받음!!"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)


#debug=True 서버 새로고침 안 해도 자동 반영