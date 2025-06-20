

$(document).ready(function () {
    var userId = $("#headUserId").val();
    var usertype = $("#headUsertype").val();
    var roomId = null
    function postToDetail(regNum) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/container/bookingDetail';

        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'param';
        input.value = regNum;
        form.appendChild(input);

        document.body.appendChild(form);
        form.submit();
    }
    

    $('#myModal').on('shown.bs.modal', function () {
        $(".messenger-scrollbar").mCustomScrollbar({
            theme: "minimal-dark",
            scrollInertia: 1500,
            autoHideScrollbar: true,
            setHeight: 540,
            scrollTo: "bottom"
        });

        $(".messenger-scrollbar").mCustomScrollbar("update");
        $(".messenger-scrollbar").mCustomScrollbar("scrollTo", "bottom");
    });


    function applyCnt(){
        $.ajax({
            url: "/applyCnt",
            method: "GET",
            data: {"userId":userId,"usertype":usertype},
            dataType: 'json',
            success: function(data) {
                var applyCnt = JSON.parse(data.cnt);
                let applyCntHtml = "";
                if (applyCnt > 0) {
                    applyCntHtml += `
                        <div class="spinner4 spinner-4"></div>
                        <div class="ntd-ctn">
                            <span>${applyCnt}</span>
                        </div>
                    `;
                    $(".applyCnt").html(applyCntHtml);
                }
            },
            error: function(request) {
                const message = request.responseJSON?.message || "서버 요청 중 오류가 발생했습니다!";
                alert(message);
            }
        });
    }

    function messengerCnt(){
        $.ajax({
            url: "/messengerCnt",
            method: "GET",
            data: {"userId":userId},
            dataType: 'json',
            success: function(data) {
                var messengerCnt = JSON.parse(data.cnt);
                let messengerCntHtml = "";
                if (messengerCnt > 0) {
                    messengerCntHtml += `
                        <div class="spinner4 spinner-4"></div>
                        <div class="ntd-ctn">
                            <span>${messengerCnt}</span>
                        </div>
                    `;
                    $(".messengerCnt").html(messengerCntHtml);
                }
            },
            error: function(request) {
                const message = request.responseJSON?.message || "서버 요청 중 오류가 발생했습니다!";
                alert(message);
            }
        });
    }

    function applyList(){
        $.ajax({
            url: "/applyList",
            method: "GET",
            data: {"userId":userId,"usertype":usertype},
            dataType: 'json',
            success: function(data) {
                var text = (usertype == "1") ? "접수 되었습니다." : "확정 되었습니다.";
                let rowsHtml = "";
                data.forEach(rows => {
                    rowsHtml += `
                        <a href="#" class="booking-link" data-reg-num="${rows[0]}"> 
                            <div class="hd-message-sn">
                                <div class="hd-mg-ctn2">
                                    <h3>[${rows[1]}] 님으로 부터</h3>
                                    <p>[${rows[2]}] 예약이 ${text}</p>
                                </div>
                            </div>
                        </a>
                        `;
                });

                $("#alarmDiv").html(rowsHtml);
                $("#alarmDiv").on("click", ".booking-link", function(event) {
                    event.preventDefault(); // <a> 태그의 기본 동작(페이지 이동) 방지

                    // 클릭된 <a> 태그에서 data-reg-num 속성 값을 가져옵니다.
                    const regNum = $(this).data('reg-num'); 
                    
                    // postToDetail 함수를 호출합니다.
                    postToDetail(regNum);
                });
            },
            error: function(request) {
                const message = request.responseJSON?.message || "서버 요청 중 오류가 발생했습니다!";
                alert(message);
            }
        });
    }

    function messengerList(){
        $.ajax({
            url: "/messengerList",
            method: "GET",
            data: {"userId":userId},
            dataType: 'json',
            success: function(data) {
                let rowsHtml = "";
                data.forEach(rows => {
                    rowsHtml += `
                        <a type="button" class="messenger-link" data-toggle="modal" data-target="#myModal" data-messenger-num="${rows[0]}">
                            <div class="hd-message-sn">
                                <div class="hd-message-img chat-img">
                                    <img src="/static/img/post/me.png" alt="">
                                    <div class="chat-avaible"><i class="notika-icon notika-dot"></i></div>
                                </div>
                                <div class="hd-mg-ctn">
                                    <h3>[${rows[1]}]</h3>
                                    <p>[${rows[2]}]님과 [${rows[3]}]님의 대화입니다. </p>
                                </div>
                            </div>
                        </a>
                    `;
                });

                $("#messengerDiv").html(rowsHtml);

              
            },
            error: function(request) {
                const message = request.responseJSON?.message || "서버 요청 중 오류가 발생했습니다!";
                alert(message);
            }
        });
    }

    if(userId != "None") {
        applyCnt();
        applyList();
        messengerCnt();
        messengerList();
    } 

    const socket = io();
        
    // const roomId = 1;  // 예시로 고정값. 동적으로 지정하려면 URL 등에서 추출

    socket.on('connect', () => {
        console.log('소켓 연결 완료');
        // socket.emit('join_room', { room_id: roomId });  // 서버에 방 입장 요청
    });

    $("#messengerDiv").on("click", ".messenger-link", function(event) {
        event.preventDefault(); 

        $("#messages").empty();
        roomId = $(this).data('messenger-num');
        socket.emit("join_room", { room_id: roomId });
    });

    socket.on('messenger_message', data => {
        const li = document.createElement('li');
        li.style.listStyle = "none"; // 불릿 제거

        if (data.id == userId) {
            // 내가 보낸 메시지 (오른쪽 정렬)
            li.innerHTML = `
                <div style="display: flex; justify-content: flex-end; margin-bottom: 8px;">
                    <div style="max-width: 45%; background-color: #daf1fc; padding: 10px; border-radius: 10px; text-align: right;">
                        <span style="font-weight: bold; color:rgb(40, 159, 214); font-size: 16px;">[${data.user}]</span>
                        <p style="margin: 4px 0;">${data.message}</p>
                        <small style="color: gray;">${data.timestamp || ''}</small>
                    </div>
                </div>
            `;
        } else {
            // 상대방이 보낸 메시지 (왼쪽 정렬)
            li.innerHTML = `
                <div style="display: flex; justify-content: flex-start; margin-bottom: 8px;">
                    <div style="max-width: 60%; background-color: #fce2e2; padding: 10px; border-radius: 10px; text-align: left;">
                        <span style="font-weight: bold; color:rgb(214, 40, 83); font-size: 16px;">[${data.user}]</span>
                        <p style="margin: 4px 0;">${data.message}</p>
                        <small style="color: gray;">${data.timestamp || ''}</small>
                    </div>
                </div>
            `;
        }

        document.getElementById('messages').appendChild(li);
        $(".messenger-scrollbar").mCustomScrollbar("update");
        $(".messenger-scrollbar").mCustomScrollbar("scrollTo", "bottom");
    });

    function send() {
        const input = document.getElementById('message');
        const messageText = input.value.trim();
        if (messageText === '') return;

        socket.emit('send_message', {
            room_id: roomId,
            message: messageText
        });
        input.value = '';
    }



    $('#myModalthree').on('shown.bs.modal', function () {
        $('#message').focus();
        
    });
    $('#message').on('keydown', function(event) {
        // Enter 키가 눌렸는지 확인 (keyCode 13 또는 event.key === 'Enter')
        if (event.keyCode === 13 || event.key === 'Enter') {
            // 이벤트 전파 중지 (버블링을 막음)
            event.stopPropagation();
            // 브라우저의 기본 동작 방지 (예: 폼 제출, 페이지 새로고침)
            event.preventDefault();

            // 메시지 전송 버튼 클릭 동작 호출
            $('#btnSend').click();

            // 또는 메시지 전송 로직을 여기에 직접 작성
            // sendMessageFunction(); // 예시: 메시지를 전송하는 함수
        }
    });
    $("#btnSend").click(function(){
        send();
    });

    
});
