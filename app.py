from flask import Flask, render_template, request, jsonify 
from flask_cors import CORS
import os
from flask_sqlalchemy import SQLAlchemy  
from flask_migrate import Migrate 
from sqlalchemy.dialects.postgresql import UUID # UUID 자료형 사용을 위함
from sqlalchemy.sql import func # func.now() 사용을 위함 
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

#* 2. Profiles (사용자 프로필) - auth.users와 1:1 관계
class Profile(db.Model):
    __tablename__ = 'profiles' # DB에 저장될 테이블 이름
    
    # id: Supabase의 인증 시스템(auth.users)과 연결되는 핵심 키입니다. 
    # 회원가입 시 생성된 UUID를 그대로 가져와서 PK(기본키)로 사용합니다.
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    
    email = db.Column(db.Text, unique=True, nullable=False) # 이메일 (중복 불가)
    nickname = db.Column(db.Text, unique=True, nullable=False) # 닉네임 (중복 불가)
    profile_img_url = db.Column(db.Text) # 프로필 이미지 경로
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) # 생성일 (자동 입력)

#* 3. Feeds (게시글 및 장소 데이터)
class Feed(db.Model):
    __tablename__ = 'feeds' # DB에 저장될 테이블 이름
    
    # 게시글 고유 번호 (1, 2, 3... 자동으로 증가)
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    
    # 작성자 ID: 누가 썼는지 알기 위해 Profile 테이블의 id를 가져와서 기록합니다 (FK)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('profiles.id'), nullable=False)
    
    title = db.Column(db.Text, nullable=False)   # 글 제목
    content = db.Column(db.Text, nullable=False) # 글 내용
    image_url = db.Column(db.Text)               # 첨부 사진 URL
    
    # -- 카카오맵 API 연동 데이터 --
    place_name = db.Column(db.Text)        # 장소 이름 (예: 스타벅스 강남점)
    road_address_name = db.Column(db.Text) # 도로명 주소
    latitude = db.Column(db.Float)         # 위도 (Y좌표)
    longitude = db.Column(db.Float)        # 경도 (X좌표)
    category_code = db.Column(db.String(10)) # 카테고리 코드 (음식점, 카페 등)
    
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) # 작성 시간

#* 4. Likes (좋아요 기능)
class Like(db.Model):
    __tablename__ = 'likes' # DB에 저장될 테이블 이름
    
    # 좋아요 기록 고유 번호
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    
    # 누가 좋아요를 눌렀는지 (Profile 테이블 참조)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('profiles.id'), nullable=False)
    
    # 어떤 글에 좋아요를 눌렀는지 (Feed 테이블 참조)
    feed_id = db.Column(db.BigInteger, db.ForeignKey('feeds.id'), nullable=False)
    
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) # 누른 시간

    # 중복 방지: 한 사람이(user_id) 같은 글(feed_id)에 좋아요를 두 번 누를 수 없게 설정합니다.
    __table_args__ = (db.UniqueConstraint('user_id', 'feed_id', name='unique_user_feed_like'),)

#* DB 파일 생성 (처음 한 번만 실행됨)
with app.app_context():
    db.create_all()
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
    port = int(os.environ.get("PORT", 5909))
    app.run(host="0.0.0.0", port=port, debug=True)
#debug=True 서버 새로고침 안 해도 자동 반영