//* html에서 불러옴
const user_text = document.querySelector("#user-text")     // content 받는 input
const save_db_button = document.querySelector("#save-db-button")   // 저장 버튼
const get_db_button = document.querySelector("#get-db-button")     // DB 내용 가져오는 버튼
const DB_plus_div = document.querySelector(".DB-plus-div")         // 받은 DB 데이터를 출력하기 위한 영역(위치) 
const img_user_input = document.querySelector("#img-user-input")   // 저장 버튼




//* 이벤트 리스너(save_db_button) - input 값 가져옴
save_db_button.addEventListener("click", async(event) =>{
    event.preventDefault()
    const live_user_text = user_text.value 
    console.log("저장 버튼 클릭", live_user_text)
// 저장 버튼을 누르면 입력한 내용의 값을(input) 변수에 저장

    //* fetch.  db_create를 연결점으로 정보를 주고(input 값) 받음(return 값)
    const response = await fetch("/feeds_input_save", {  // db_create 어딨니! 
        method : "POST",
        headers : { "Content-Type": "application/json" }, 
        body: JSON.stringify({ "message": live_user_text }) //* 보낼거
        })

    const json_response = await response.json() //* 받은거
    console.log(json_response)
})
//// 버튼 이벤트 감지 -> 사용자가 input에 입력한걸(content) 가져와서 
//// 그걸 python에 보내고, 잘 받았다는 값을 받는 것



//* 이벤트 리스너(get_db_button) - 버튼 클릭 시 DB 내용 출력
get_db_button.addEventListener("click", async (event) => {
    event.preventDefault();

    try {
        const receive = await fetch("/db_read");
        const json_receive = await receive.json(); // 서버에서 리스트 형태로 준다고 가정
        console.log("DB 받음~", json_receive);

        // 비워주고 새로 그리기
        DB_plus_div.innerHTML = ""; 

        // 데이터가 있다면 반복문으로 다 보여주기
        json_receive.forEach(item => {
            const h1 = document.createElement("h1");
            h1.textContent = item.content; // 안전하게 textContent 사용
            DB_plus_div.appendChild(h1);
        });

    } catch (error) {
        console.error("데이터 가져오기 실패!", error);
    }
});
//// 데이터 베이스에 있는 내용을 읽어서 출력(반복문 사용하여 줄줄히 출력)



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


//* 이벤트 리스너(get_db_button) - 버튼 클릭 시 DB 내용 출력
img_user_input.addEventListener("click", async (event) => {
    event.preventDefault();

    if (file && file.type.startsWith('image/')) {
        console.log("올바른 이미지 파일입니다. ✅");
        // 여기에 미리보기 코드를 넣으면 됩니다.
    } else {
        alert("이미지 파일만 올려주세요! ❌");
        fileInput.value = ""; // 잘못된 파일이면 선택 취소
    }

});
