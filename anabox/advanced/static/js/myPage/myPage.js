

$(document).ready(function () {
    // const regNum = $("#regNum").val();
    // const userId = $("#userId").val();

    // 뒤로
    $('#btnBack').on('click', function(e) {
        history.back();
    });

    $('#userPhone').add('#companyPhone').on('input', function () {
        let value = $(this).val().replace(/[^0-9]/g, ''); // 숫자만
        let result = '';

        if (value.length < 4) {
            result = value;
        } else if (value.length < 8) {
            result = value.slice(0, 3) + '-' + value.slice(3);
        } else {
            result = value.slice(0, 3) + '-' + value.slice(3, 7) + '-' + value.slice(7, 11);
        }

        $(this).val(result);
    });

    $('#companyFax').on('input', function () {
        let value = $(this).val().replace(/[^0-9]/g, '');
        let result = '';

        if (value.length < 3) {
            result = value;
        } else if (value.length < 7) {
            result = value.slice(0, 2) + '-' + value.slice(2);
        } else {
            result = value.slice(0, 2) + '-' + value.slice(2, 6) + '-' + value.slice(6, 10);
        }

        $(this).val(result);
    });
    

    $('#btnDelete').on('click', function(e) {
        swal({   
            title: "회원 탈퇴",   
            text: "회원 탈퇴 하시겠습니까?",   
            type: "warning",   
            showCancelButton: true,   
            confirmButtonText: "예",
            cancelButtonText: "아니요",
        }).then(function(){
            var userid = $('#userid').val().trim();
            $.ajax({
                url: "/auth/delete",
                method: "POST",
                data: {"userid":userid} ,
                dataType: "json",
                success: function (data) {
                    if (data.cnt > 0){
                        swal("회원 탈퇴", data.message, "warning")
                    } else{
                        swal("회원 탈퇴", data.message, "success")
                        .then(function() {
                        window.location.href = "/auth/logout";  
                        });
                    }
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
			title: "회원 정보 수정",   
			text: "회원 정보 수정 페이지를 불러오시겠습니까?",   
			type: "warning",   
			showCancelButton: true,   
			confirmButtonText: "예",
            cancelButtonText: "아니요",
		}).then(function(){
            swal("수정", "수정 가능한 상태입니다.", "success")
            const ids = [
                        "userName",
                        "userEmail",
                        "userPhone",
                        "userCompany",
                        "companyIntro",
                        "ceoName",
                        "companyPhone",
                        "companyFax",
                        "companyEmail",
                        "companyHomepage",
                        "companyAddressdetail"
                        ];
            ids.forEach(function(id) {
                document.getElementById(id).readOnly = false;
            });

            $('#btnAddress').show();
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
                window.location.href = "/auth/myPage"; 
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
            
            var userid = $('#userid').val().trim();
            var userName = $('#userName').val().trim();
            var userEmail = $('#userEmail').val().trim();
            var userPhone = $('#userPhone').val().trim();
            var userCompany = $('#userCompany').val().trim();
            var companyPhone = $('#companyPhone').val().trim();
            var companyEmail = $('#companyEmail').val().trim();
            var companyFax = $('#companyFax').val().trim();
            if (!userid || !userName || !userEmail || !userPhone || !userCompany ) {
                e.preventDefault(); // 폼 제출 막기
    
                let emptyFields = [];
                if (!userid) emptyFields.push("아이디")
                if (!userName) emptyFields.push("사용자 이름")
                if (!userEmail) emptyFields.push("이메일")
                if (!userPhone) emptyFields.push("휴대폰 번호")
                if (!userCompany) emptyFields.push("회사명")
                
    
                const message = emptyFields.join(', ') + "을(를) 입력해 주세요.";
                swal(message); // sweetalert 또는 alert(message)
                return false;
            }

            const phoneRegex = /^01[016789]-\d{3,4}-\d{4}$/;
            if (!phoneRegex.test(userPhone)) {
                swal("휴대폰 번호 형식이 올바르지 않습니다. (예: 010-1234-5678)");
                return;
            }

            if (companyPhone && !phoneRegex.test(companyPhone)) {
                swal("회사 전화 번호 형식이 올바르지 않습니다. (예: 010-1234-5678)");
                return;
            }
            const faxRegex = /^(0\d{1,2})-\d{3,4}-\d{4}$/;
            if (companyFax && !faxRegex.test(companyFax)) {
                swal("팩스 번호 형식이 올바르지 않습니다. 예: 02-1234-5678");
                return;
            }
            
            const eMailregex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!eMailregex.test(userEmail)) {
                swal("이메일 형식이 올바르지 않습니다. (예: abcd@efgh.com)");
                return;
            }

            if (companyEmail && !eMailregex.test(companyEmail)) {
                swal("회사 이메일 형식이 올바르지 않습니다. (예: abcd@efgh.com)");
                return;
            }


            const form = $('#myPage');
            const formData = form.serialize();
    
            $.ajax({
                url: "/auth/myPage",
                method: "POST",
                data: formData,
                dataType: "json",
                success: function (data) {
                    swal("수정", data.message, "success")
                    .then(function() {
                        window.location.href = "/auth/myPage"; 
                    });
                },
                error: function (request) {
                    const message = request.responseJSON?.message || "서버 요청 중 오류가 발생했습니다!";
                    swal(message);
                }
            });
        });
    });
    
    $('#btnAddress').on('click', function(e) {
        new daum.Postcode({
            oncomplete: function(data) {
                var addr = ''; // 주소 변수

                if (data.userSelectedType === 'R') { // 사용자가 도로명 주소를 선택했을 경우
                    addr = data.roadAddress;
                } else { // 사용자가 지번 주소를 선택했을 경우(J)
                    addr = data.jibunAddress;
                }

                document.getElementById("companyAddress").value = addr;
                // 커서를 상세주소 필드로 이동한다.
                document.getElementById("companyAddressdetail").focus();
            }
        }).open();
    });


});









