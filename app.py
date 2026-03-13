import sqlite3
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

# JSON 응답 시 한글 깨짐 방지
app.json.ensure_ascii = False

# [추가] 데이터베이스 초기화 함수: 서버가 켜질 때 테이블(그릇)을 만듭니다.
def init_db():
    conn = sqlite3.connect("practice.db")
    cur = conn.cursor()
    # logs 테이블이 없으면 생성합니다. id는 자동 번호, content는 글자 저장 칸입니다.
    cur.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT
        )
    """)
    conn.commit()
    conn.close()

# 앱이 시작될 때 위 함수를 실행해서 DB 설계를 완료합니다.
init_db()

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/get_test", methods=["GET"])
def get_test():
    # 나중에는 여기서 DB 데이터를 꺼내서(SELECT) 전달하게 될 거예요!
    return jsonify({
        "name": "self.response(909)",
        "team": ["팀장님", "오른팔", "왼팔"]
    })

@app.route("/post_test", methods=["POST"])
def post_test():
    # 1. 브라우저에서 보낸 JSON 데이터 받기
    request_data = request.get_json()
    real_msg = request_data.get("msg")

    # 2. DB 연결 (통로 열기)
    conn = sqlite3.connect("practice.db")
    cur = conn.cursor()

    # 3. 안전하게 저장 (플레이스홀더 ? 사용)
    # SQL 문장은 따옴표 안에서 깔끔하게 마무리하고, 데이터는 뒤에 따로 넘겨줍니다.
    cur.execute("INSERT INTO logs (content) VALUES (?)", (real_msg,))

    # 4. 저장 확정 및 통로 닫기
    conn.commit()
    conn.close()

    return jsonify({
        "message": f"DB 저장 성공: {real_msg}"
    })
    
if __name__ == "__main__":
    app.run(debug=True, port=8000)