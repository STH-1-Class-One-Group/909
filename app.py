# 1. 라이브러리 임포트 (가져오기)
# [가져온 곳]: 설치한 파이썬 패키지(flask, flask_sqlalchemy, flask_cors)에서 가져옴
from flask import Flask, render_template, jsonify  # Flask: 웹 서버 몸체 / render_template: HTML 출력 / jsonify: JSON 응답용
# from flask_sqlalchemy import SQLAlchemy            # SQLAlchemy: 파이썬 코드로 DB를 조작하게 해주는 도구(ORM)
from flask_cors import CORS                        # CORS: 다른 도메인(Cloudflare 등)의 접속을 허용해주는 보안 설정                          # os: 내 컴퓨터의 파일 경로를 계산하기 위한 파이썬 내장 모듈

# 2. Flask 앱 생성 및 설정
# [의미]: 서버의 중심 객체를 생성하고, DB 파일의 위치를 지정함
app = Flask(__name__) # [커스텀]: 프로젝트 규모가 커지면 이름을 바꿀 수 있지만 기본적으로 __name__을 사용함
CORS(app)             # [종뉴]: 보안 관련 설정 명령어. 외부 서비스와 통신하려면 필수임

# [내용]: DB 파일의 저장 경로를 설정함 (현재 폴더에 team.db라는 이름으로 생성)
# basedir = os.path.abspath(os.path.dirname(__file__)) 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'team.db') # [커스텀]: 'team.db' 부분을 원하는 파일명으로 변경 가능
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # [의미]: 불필요한 이벤트 알림을 꺼서 서버 성능을 높임

# db = SQLAlchemy(app) # [의미]: 위 설정을 바탕으로 DB 조작 객체를 생성함

# # 3. 데이터베이스 모델(설계도) 정의
# # [의미]: DB에 어떤 표(Table)를 만들지 결정하는 클래스 명령어
# class User(db.Model):
#     # [내용]: 표의 칸(Column)을 정의함
#     id = db.Column(db.Integer, primary_key=True)      # 고유 번호 (중복 불가)
#     username = db.Column(db.String(10), nullable=False) # [커스텀]: 80은 최대 글자수. 필요에 따라 조절 가능
    # message = db.Column(db.String(200))               # [커스텀]: 팀 프로젝트에 필요한 필드(나이, 이메일 등)로 자유롭게 변경 가능

# 4. 웹 주소(Route)와 기능 연결
# [의미]: 사용자가 특정 주소로 들어왔을 때 실행할 함수를 지정함

# (1) 메인 화면 주소: http://localhost:8000/
@app.route("/") # [종류]: 라우팅 명령어. "/"는 첫 페이지를 의미함
def home():
    # [내용]: templates 폴더 안의 특정 파일을 찾아서 브라우저에 보여줌
    # [커스텀]: "index.html" 외에 다른 파일명으로 바꿀 수 있음 (단, templates 폴더 안에 있어야 함)
    return render_template("index.html") 

# (2) 데이터 확인 주소: http://localhost:8000/api/hello
@app.route("/api/hello") # [커스텀]: 주소 이름을 "/api/test" 등으로 자유롭게 변경 가능
def hello():
    # [내용]: 파이썬의 딕셔너리 데이터를 JSON 형식의 문자열로 변환하여 전송함
    # [커스텀]: {"message": "..."} 안의 내용을 팀 프로젝트 데이터에 맞게 수정 가능
    return jsonify({"message": "Hello World from Flask!"})

# 5. 서버 실행부
# [의미]: 이 파일이 직접 실행될 때만 서버를 가동함
if __name__ == "__main__":
    # [내용]: 앱 컨텍스트 안에서 DB 테이블이 없다면 자동으로 생성함
    # with app.app_context():
        # db.create_all() 
    
    # [옵션]: debug=True는 코드 수정 시 자동 재시작 / port=8000은 접속 포트 번호
    # [커스텀]: 포트 번호가 충돌나면 5000, 8080 등으로 변경 가능함
    app.run(debug=True, port=8000)