

$(document).ready(function () {
    const regNum = $("#regNum").val();
    const userId = $("#userId").val();
    const registerId = $("#registerId").val();

    const noSpaceFields = [
    "tareWeight", "pricePerDay", 
    "containerNumber", "size", "terminal", "location", "portType"
    ];

    const blockAllKeyboardFields = ['availableFrom', 'availableTo'];

    function formatNumberInput(input) {
        const raw = input.value.replace(/\s+/g, "").replace(/[^0-9]/g, "");
        const formatted = raw.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        input.value = formatted;
    }

    // 공백 및 스페이스 차단 (noSpaceFields)
    noSpaceFields.forEach(id => {
        const input = document.getElementById(id);
        if (!input) return;
        input.addEventListener("keydown", function(e) {
            if (e.key === " " || e.code === "Space") {
            e.preventDefault();
            }
        });
    });

    // 숫자 포맷 적용 (tareWeight, pricePerDay)
    ["tareWeight", "pricePerDay"].forEach(id => {
        const input = document.getElementById(id);
        if (!input) return;
        input.addEventListener("input", function() {
            formatNumberInput(this);
        });
    });

    // 날짜 필드 키보드 입력 완전 차단 (availableFrom, availableTo)
    blockAllKeyboardFields.forEach(id => {
        const input = document.getElementById(id);
        if (!input) return;
        input.addEventListener("keydown", function(e) {
            e.preventDefault();
        });
    });


    function postToDetail(regNum) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/container/containerDetail';

        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'param';
        input.value = regNum;
        form.appendChild(input);

        document.body.appendChild(form);
        form.submit();
    }

    function postToBookingDetail(regNum) {
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

    function postToCompany(userId) {
        const form = document.createElement('form');
        form.method = 'post';
        form.action = '/company/company';

        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'userId';  // 서버에서 받는 파라미터 이름과 동일하게
        input.value = userId;
        form.appendChild(input);

        document.body.appendChild(form);
        form.submit();
    }
    // 뒤로
    $('#btnBack').on('click', function(e) {
        history.back();
    });
    
    $('#btnCompany').on('click', function(e) {
        postToCompany(registerId)
    });



    // 등록페이지 이동
    $('#btnRegister').on('click', function(e) {
         swal({   
			title: "컨테이너 등록",   
			text: "등록페이지로 이동 하시겠습니까?",   
			type: "warning",   
			showCancelButton: true,   
			confirmButtonText: "예",
            cancelButtonText: "아니요",
		}).then(function(){
            window.location.href = "/container/register";
        });
    });

    // 해당 컨테이너 삭제
    $('#btnDelete').on('click', function(e) {
    swal({   
        title: "컨테이너 삭제",   
        text: "해당 컨테이너를 삭제 하시겠습니까?",   
        type: "warning",   
        showCancelButton: true,   
        confirmButtonText: "예",
        cancelButtonText: "아니요",
    }).then(function(){
        $.ajax({
            url: "/container/delete",
            method: "POST",
            data: {"regNum":regNum, "userId":userId} ,
            dataType: "json",
            success: function (data) {
                swal("삭제", data.message, "success")
                .then(function() {
                    window.location.href = "/container/containerList";  
                });
            },
            error: function (request) {
                const message = request.responseJSON?.message || "서버 요청 중 오류가 발생했습니다!";
                swal(message);
            }
        });
    });
       
    });

    $('#btnModify').on('click', function(e) {

        swal({   
			title: "컨테이너 수정",   
			text: "수정 페이지를 불러오시겠습니까?",   
			type: "warning",   
			showCancelButton: true,   
			confirmButtonText: "예",
            cancelButtonText: "아니요",
		}).then(function(){
            swal("수정", "수정 가능한 상태입니다.", "success")
            const ids = ["containerNumber","size","tareWeight","terminal","location","portType","availableFrom","availableTo","pricePerDay","remarks"];
            ids.forEach(function(id) {
                document.getElementById(id).readOnly = false;
            });

            $("#beforeBtnModify").attr("hidden", true);
            $("#afterBtnModify").attr("hidden", false)
        });

    });

    $('#btnCancel').on('click', function(e) {
        swal({   
			title: "컨테이너 수정 취소",   
			text: "수정을 취소 하시겠습니까?",   
			type: "warning",   
			showCancelButton: true,   
			confirmButtonText: "예",
            cancelButtonText: "아니요",
		}).then(function(){
            swal("수정", "수정 불가능한 상태입니다.", "success")
            .then(function(){
                postToDetail(regNum);
            });
        });
    });
    
    $('#btnUpdate').on('click', function(e) {
        swal({   
			title: "컨테이너 수정",   
			text: "컨테이너를 수정 하시겠습니까?",   
			type: "warning",   
			showCancelButton: true,   
			confirmButtonText: "예",
            cancelButtonText: "아니요",
		}).then(function(){
            e.preventDefault();  // 폼 기본 제출 막기
        
            var userId = $('#userId').val().trim()
            var containerNumber = $('#containerNumber').val().trim()
            var size = $('#size').val().trim()
            var tareWeight = $('#tareWeight').val().trim()
            var terminal = $('#terminal').val().trim()
            var location = $('#location').val().trim()
            var portType = $('#portType').val().trim()
            var availableFrom = $('#availableFrom').val().trim()
            var availableTo = $('#availableTo').val().trim()
            var pricePerDay = $('#pricePerDay').val().trim()
    
            if (!containerNumber || !size || !tareWeight || !terminal || !location || !portType || !availableFrom || !availableTo || !pricePerDay ) {
                e.preventDefault(); // 폼 제출 막기
    
                let emptyFields = [];
                if (!containerNumber) emptyFields.push("컨테이너 번호")
                if (!size) emptyFields.push("사이즈")
                if (!tareWeight) emptyFields.push("무게(kg)")
                if (!terminal) emptyFields.push("터미널")
                if (!location) emptyFields.push("지역")
                if (!portType) emptyFields.push("항구 타입")
                if (!availableFrom) emptyFields.push("시작일")
                if (!availableTo) emptyFields.push("종료일")
                if (!pricePerDay) emptyFields.push("일일 가격(KRW)")
                
    
                const message = emptyFields.join(', ') + "을(를) 입력해 주세요.";
                swal(message); // sweetalert 또는 alert(message)
                return false;
            }
    
            if(!userId){
                e.preventDefault(); // 폼 제출 막기
    
                const message = "로그인 정보가 없습니다. 관리자에게 문의하세요.";
                swal(message); // sweetalert 또는 alert(message)
                return false;
            }
            
            if (availableFrom && availableTo) {
                const fromDate = new Date(availableFrom);
                const toDate = new Date(availableTo);
                if (fromDate > toDate) {
                    swal("시작일은 종료일보다 늦을 수 없습니다.");
                    return false;  // 제출 중단
                }
            }
    
            const form = $('#detailForm');
            const formData = form.serialize();
    
            $.ajax({
                url: "/container/update",
                method: "POST",
                data: formData,
                dataType: "json",
                success: function (data) {
                    swal("수정", data.message, "success")
                    .then(function() {
                        postToDetail(regNum);
                    });
                },
                error: function (request) {
                    const message = request.responseJSON?.message || "서버 요청 중 오류가 발생했습니다!";
                    swal(message);
                }
            });
        });
    });

    // 예약 신청
    $('#btnBookingApply').on('click', function(e) {
        swal({   
			title: "예약 신청",   
			text: "예약 신청 하시겠습니까?",   
			type: "warning",   
			showCancelButton: true,   
			confirmButtonText: "예",
            cancelButtonText: "아니요",
		}).then(function(){
            const form = $('#detailForm');
            const formData = form.serialize();
            $.ajax({
                url: "/container/bookingApply",
                method: "POST",
                data: formData,
                dataType: "json",
                success: function (data) {
                    swal("예약 신청", data.message, "success")
                    .then(function() {
                        postToBookingDetail(regNum);
                    });
                },
                error: function (request) {
                    const message = request.responseJSON?.message || "서버 요청 중 오류가 발생했습니다!";
                    swal(message);
                }
            });
        });
    });

});









