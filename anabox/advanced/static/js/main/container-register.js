

$(document).ready(function () {

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



    // $('#registerForm').on('submit', function (e) {
        

    //     if (!containerNumber || !size || !tareWeight || !terminal || !location || !portType || !availableFrom || !availableTo || !pricePerDay ) {
    //         e.preventDefault(); // 폼 제출 막기

    //         let emptyFields = [];
    //         if (!containerNumber) emptyFields.push("컨테이너 번호")
    //         if (!size) emptyFields.push("사이즈")
    //         if (!tareWeight) emptyFields.push("무게(kg)")
    //         if (!terminal) emptyFields.push("터미널")
    //         if (!location) emptyFields.push("지역")
    //         if (!portType) emptyFields.push("항구 타입")
    //         if (!availableFrom) emptyFields.push("시작일")
    //         if (!availableTo) emptyFields.push("종료일")
    //         if (!pricePerDay) emptyFields.push("일일 가격(KRW)")
            

    //         const message = emptyFields.join(', ') + "을(를) 입력해 주세요.";
    //         swal(message); // sweetalert 또는 alert(message)
    //         return false;
    //     }

    //     if(!userId){
    //         e.preventDefault(); // 폼 제출 막기

    //         const message = "로그인 정보가 없습니다. 관리자에게 문의하세요.";
    //         swal(message); // sweetalert 또는 alert(message)
    //         return false;
    //     }
    // });
    
    $('#submitBtn').on('click', function(e) {
        swal({   
			title: "컨테이너 등록",   
			text: "등록 하시겟습니까?",   
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
            
            const form = $('#registerForm');
            const formData = form.serialize();
        
            $.ajax({
                "url": "/container/register",
                "method": "POST",
                "data" : formData,
                "dataType": 'json',
                "success": function(data, status, xhr) {
                    const message = data.message;

                    swal("등록", message, "success")
                    .then(function() {
                        window.location.href = "/container/containerList";  
                    });
                    // 필요시 성공 후 폼 초기화 또는 페이지 이동 처리 가능
                    $('#registerForm')[0].reset();
                },
                "error": function(request) {
                    const message = request.responseJSON?.message || "서버 요청 중 오류가 발생했습니다!.";
                    swal(message);
                }
            });
		});
    });
});









