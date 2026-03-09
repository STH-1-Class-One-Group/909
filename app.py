from flask import Flask
import os

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello world"

@-.route('/') #GET 요청용
def GET_choose():
    return "GET 받음!!"


@-.route('/') #POST 요청용
def POST_choose():
    return "POST 받음!!"



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


