

$(document).ready(function () {
    var chkId = 'N';
    var chkPw = 'N';

    $("#chkId").on("click",function(){
        var userId = $('#userId').val().trim();
        if(!userId){
            swal("아이디를 입력해주세요.");
            return;
        }

        if (chkId == 'N'){
            $.ajax({
                url: "/auth/chkId",
                method: "GET",
                data: {"userId": userId },
                dataType: "json",
                success: function (data) {
                    if(data.idCnt > 0){
                         swal("이미 등록 된 아이디 입니다.");
                    } else {
                        swal({   
                            title: "아이디 확인",   
                            text: "사용 가능한 아이디 입니다. 사용 하시겠습니까?",   
                            type: "warning",   
                            showCancelButton: true,   
                            confirmButtonText: "예",
                            cancelButtonText: "아니요",
                        }).then(function (result) {
                            chkId = 'Y';
                            $('#userId').prop('readonly', true);
                            $('#chkId')
                            .removeClass('btn btn-warning notika-btn-warning btn-sm waves-effect')
                            .addClass('btn btn-info notika-btn-info btn-sm waves-effect');
                            $('#chkId').text("아이디 수정");
                        })
                    }
                },
                error: function (request) {
                    const message = request.responseJSON?.message || "서버 요청 중 오류가 발생했습니다!";
                    swal(message);
                }
            });
        } else {
           swal({   
                title: "아이디 수정",   
                text: "현재 아이디는 사용 가능합니다. 수정하시겠습니까?",   
                type: "warning",   
                showCancelButton: true,   
                confirmButtonText: "예",
                cancelButtonText: "아니요",
            }).then(function (result) {
                chkId = 'N';
                swal("수정 가능합니다.");
                $('#userId').prop('readonly', false);
                $('#chkId')
                .removeClass('btn btn-info notika-btn-info btn-sm waves-effect')
                .addClass('btn btn-warning notika-btn-warning btn-sm waves-effect');
                $('#chkId').text("아이디 확인");
            }) 
        }
    })

    $("#chkPw").on("click",function(){
        var password = $('#password').val().trim();
        var password2 = $('#password2').val().trim();
        let emptyFields = [];
        if (!password) emptyFields.push("비밀번호");
        if (!password2) emptyFields.push("비밀번호 확인");
        if (emptyFields.length > 0) {
            const message = emptyFields.join(', ') + "을(를) 입력해 주세요.";
            swal(message);
            return;
        }
        if (chkPw == 'N'){
            if (password !== password2) {
                swal("비밀번호가 일치하지 않습니다.");
                return;
            } else {
                chkPw = 'Y';
                swal("비밀번호가 일치합니다.");
                $('#password').prop('readonly', true);
                $('#password2').prop('readonly', true);
                $('#chkPw')
                .removeClass('btn btn-warning notika-btn-warning btn-sm waves-effect')
                .addClass('btn btn-info notika-btn-info btn-sm waves-effect');
                $('#chkPw').text("비밀번호 수정");
            }
        } else {
            swal({   
                title: "비밀번호 수정",   
                text: "현재 비밀번호는 일치합니다. 수정하시겠습니까?",   
                type: "warning",   
                showCancelButton: true,   
                confirmButtonText: "예",
                cancelButtonText: "아니요",
            }).then(function (result) {
                chkPw = 'N';
                swal("수정 가능합니다.");
                $('#password').prop('readonly', false);
                $('#password2').prop('readonly', false);
                $('#chkPw')
                .removeClass('btn btn-info notika-btn-info btn-sm waves-effect')
                .addClass('btn btn-warning notika-btn-warning btn-sm waves-effect');
                $('#chkPw').text("비밀번호 확인");
            })
        }
    });

    $('#phone').on('input', function () {
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


    $('#registerForm').on('submit', function (e) {
        e.preventDefault(); // 기본 제출 막기

        const form = this; // 폼 참조 저장

        swal({   
            title: "회원 가입",   
            text: "회원 가입 하시겠습니까?",   
            type: "warning",   
            showCancelButton: true,   
            confirmButtonText: "예",
            cancelButtonText: "아니요",
        }).then(function (result) {

            if (result) {
                var userId = $('#userId').val().trim();
                var userName = $('[name="userName"]').val().trim();
                var company = $('[name="company"]').val().trim();
                var phone = $('[name="phone"]').val().trim();
                var eMail = $('[name="eMail"]').val().trim();
                var password = $('#password').val().trim();
                var password2 = $('#password2').val().trim();
                var userType = $('#userType').val().trim();

                // 빈 값 체크
                let emptyFields = [];
                if (!userId) emptyFields.push("아이디");
                if (!userName) emptyFields.push("이름");
                if (!company) emptyFields.push("회사");
                if (!phone) emptyFields.push("휴대폰 번호");
                if (!eMail) emptyFields.push("이메일");
                if (!password) emptyFields.push("비밀번호");
                if (!password2) emptyFields.push("비밀번호 확인");
                if (!userType) emptyFields.push("사용자 유형");

                if (emptyFields.length > 0) {
                    const message = emptyFields.join(', ') + "을(를) 입력해 주세요.";
                    swal(message);
                    return;
                }
                
                if (chkId == 'N'){
                    swal("아이디 확인을 해주세요");
                    return;
                }

                const phoneRegex = /^01[016789]-\d{3,4}-\d{4}$/;
                if (!phoneRegex.test(phone)) {
                    swal("휴대폰 번호 형식이 올바르지 않습니다. (예: 010-1234-5678)");
                    return;
                }
                
                const eMailregex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!eMailregex.test(eMail)) {
                    swal("이메일 형식이 올바르지 않습니다. (예: abcd@efgh.com)");
                    return;
                }

                if (chkPw == 'N'){
                    swal("비밀번호 확인을 해주세요");
                    return;
                }

                if (password !== password2) {
                    swal("비밀번호가 일치하지 않습니다.");
                    return;
                }
                
                // 모든 조건 만족 → 수동 제출
                form.submit();
            }
        });
    });


    $('#loginForm').on('submit', function (e) {
        var userId = $('[name="userId"]').val().trim();
        var password = $('[name="password"]').val().trim();

        if (!userId || !password) {
            e.preventDefault(); // 폼 제출 막기

            let emptyFields = [];
            if (!userId) emptyFields.push("아이디");
            if (!password) emptyFields.push("비밀번호");

            const message = emptyFields.join(', ') + "을(를) 입력해 주세요.";
            swal(message); // sweetalert 또는 alert(message)
            return false;
        }
    });
});







