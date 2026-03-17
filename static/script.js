//* html에서 불러옴
const input_content = document.querySelector("#input-content")     // content 받는 input
const save_db_button = document.querySelector("#save-db-button")   // 저장 버튼
const get_db_button = document.querySelector("#get-db-button")     // DB 내용 가져오는 버튼
const DB_plus_div = document.querySelector(".DB-plus-div")         // 받은 DB 데이터를 출력하기 위한 영역(위치) 
//// 불러오면서 .value 쓰면 새로고침 할 때 마다 들어온 값을 변수에 저장함



//* 이벤트 리스너(save_db_button) - input 값 가져옴
save_db_button.addEventListener("click", async(event) =>{
    event.preventDefault()
    const live_input_content = input_content.value 
    console.log("버튼 클릭", live_input_content)
//// live_input_content : input_content의 값(버튼 클릭 시 입력된 값)을 저장

    //* fetch.  db_create를 연결점으로 정보를 주고(input 값) 받음(return 값)
    const response = await fetch("/db_create", {  // db_create 어딨니! 
        method : "POST",
        headers : { "Content-Type": "application/json" }, 
        body: JSON.stringify({ "message": live_input_content }) //* 보낼거
        })

    const json_response = await response.json() //* 받은거
    console.log(json_response)
})
//// event.preventDefault() // 이 친구는 form 방해꾼임. 일 못 하게 괴롭힘
//// response : input 보내고 받은 답 (db_create 함수 return 값)
//// json_response :  response를 json으로 바꿈(DB 저장 확인)



//* 이벤트 리스너(get_db_button) - 버튼 클릭 시 DB html 생김
get_db_button.addEventListener("click", async(event) =>{
    event.preventDefault()

    //* fetch.  db_read를 연결점으로 정보를 받음(GET)
    const receive = await fetch("/db_read") // db_read 저요!! //* 받은거
    const json_receive = await receive.json() 
    console.log("db 받음~", json_receive)

    DB_plus_div.innerHTML = `<h1>${json_receive[1].content}</h1>`
})
//// receive : 받은 정보(DB)
//// json_receive : receive를 json으로 바꿈(db 정보)



// 버튼 클릭 시 실행될 함수
async function getData(type) {
    const displayDiv = document.getElementById('display');
    displayDiv.innerText = '서버에 요청 중...';
    const url = type === 'success' ? '/api/hello' : '/api/fail';
    
    try {
        const response = await fetch(url);
        
        // response.ok는 상태 코드가 200~299일 때 true입니다.
        if (!response.ok) {
            throw new Error(`서버 에러 발생! (상태 코드: ${response.status})`);
        }

        const data = await response.json();
        displayDiv.style.color = 'blue';
        displayDiv.innerText = `성공 메시지: ${data.message}`;
        
    } catch (error) {
        displayDiv.style.color = 'red';
        displayDiv.innerText = `에러 내용: ${error.message}`;
        console.error('상세 에러:', error);
    }
}