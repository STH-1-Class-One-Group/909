from flask import Flask, render_template, request, jsonify 
from flask_cors import CORS
import os
from flask_sqlalchemy import SQLAlchemy  
from flask_migrate import Migrate 
from dotenv import load_dotenv  


app = Flask(__name__) #서버 객체
CORS(app)

load_dotenv() #env 파일을 함수 호출을 통해 os에 등록(불러옴)
database_url = os.getenv("DB_URL") 
#// database_url : getenv로 os 안에서 DB_URL을 뽑아옴.


#* DB 파일 경로 설정 (supabase 사용 시 여기만 변경)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"connect_args": {"connect_timeout": 10}} #
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)  
migrate = Migrate(app, db)
#// SQLALCHEMY_ENGINE_OPTIONS : 응답 없으면 포기. (10초만 기다림. 연결 실패시 실패 메시지 보내줌)
#// SQLALCHEMY_DATABASE_URI : DB 만들 때 쓸 URL 넣는곳(env를 이용해 보안 문제 막음)
#// SQLALCHEMY_TRACK_MODIFICATIONS : 데이터가 바뀌는걸 실시간으로 감지할까? ㄴㄴ (commit 할 때만 기록)
#// 스키마 추가 시 migrate를 사용하여 변경 사항을 감지하고 업데이트(삭제/추가). 내 파이썬 코드와 DB의 최종 상태를 똑같이 동기화


#* DB 스키마(설계도)
class Human(db.Model):
    id = db.Column(db.Integer, primary_key=True)      
    content = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=True)
#// id(고유 번호) : 숫자를 자동으로 매겨서 고유번호 만들거임(자동 생성)
#// content(내용) :  저장할 글자 받을거임. 200자 이내로 받을거고, 받은 답 없으면 에러낼거임!!
#// age(나이) :  숫자 받을거고, 받은 답 없어도 괜찮음.


#* DB 파일 생성 (처음 한 번만 실행됨)
with app.app_context():
    print("--- DB 테이블 생성 시도 중... ---")
    db.create_all()
    print("--- DB 테이블 생성 완료! ---")
#// config 가져와서(with) 읽고(app_context) 주소만 가져와서 그 주소에 설계도에 있는 모든걸 만들어낼거야!(파일 생성 + 내용)
#// 다 쓰면 다시 되돌려놓을게(with)


#* 주소 접속 시 index.html을 띄워줌
@app.route('/')
def index(): 
    return render_template('index.html') 


#* 받은 데이터 DB에 저장
@app.route('/db_create', methods=['POST'])  # db_create 저요!!!
def db_create():
    data = request.get_json() #* fetch로 받아냄.
    input_content = data.get("message")
    
    # DB 장부에 추가
    add_data = Human(content = input_content) 
    db.session.add(add_data)
    db.session.commit() 
    
    return jsonify({"result": "success", "message": "DB에 잘 들어갔어요!"}) #* 받았으면 줘야함 
#// db_create : 받은 데이터를 값만 뽑아 DB에 저장
#// data : input값을 fetch로 받아(request) 가져와서 JSON으로 변환
#// input_content : data에서 message라는 key로 값만 뽑아냄.
#// add_data : Human class 안의 content 항목에 input_content를 넣음
#// add(스테이징), commit(여기서는 최종 저장 역할도 함)
#// json으로 변환 후 return 반환(js에 전송)


#* DB에서 데이터 읽은 뒤 브라우저로 보냄.  (GET이니까 답 안 받음)
@app.route('/db_read', methods=['GET'])  # db_read 어디있니!, 데이터를 일방적으로 보냄(GET) 
def db_read():
    db_all = Human.query.all()
    result = []
    for split_db in db_all : 
        result.append ({
            "id" : split_db.id,
            "content" : split_db.content,
            "age" : split_db.age
        })
    print(result)
    return jsonify(result) 
#// db_read : DB 데이터 덩어리를 받아와서 쪼갠 뒤 항목별로 나눠 담아(id, content, age) json으로 변환 -> return
#// db_all : db 안에 있는 모든 내용을 가져옴
#// split_db : for 문을 통해 db_all에 있는 데이터를 하나씩 꺼내옴
#// result : js로 보낼거(항목별로 데이터를 예쁘게 나눠담음)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
#debug=True 서버 새로고침 안 해도 자동 반영