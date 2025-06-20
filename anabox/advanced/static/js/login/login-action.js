

// $(document).ready(function () {
    
//     $('#registerForm').on('submit', function (e) {
//         var userId = $('#userId').val().trim();
//         var userName = $('[name="userName"]').val().trim();
//         var company = $('[name="company"]').val().trim();
//         var eMail = $('[name="eMail"]').val().trim();
//         var password = $('#password').val().trim();
//         var userType = $('#userType').val().trim();

//         if (!userId || !userName || !company ||!eMail || !password || !userType) {
//             e.preventDefault(); // 폼 제출 막기

//             let emptyFields = [];
//             if (!userId) emptyFields.push("아이디");
//             if (!userName) emptyFields.push("이름");
//             if (!company) emptyFields.push("회사");
//             if (!eMail) emptyFields.push("이메일");
//             if (!password) emptyFields.push("비밀번호");
//             if (!userType) emptyFields.push("사용자 유형");

//             const message = emptyFields.join(', ') + "을(를) 입력해 주세요.";
//             swal(message); // sweetalert 또는 alert(message)
//             return false;
//         }
//     });

//     $('#loginForm').on('submit', function (e) {
//         var userId = $('[name="userId"]').val().trim();
//         var password = $('[name="password"]').val().trim();

//         if (!userId || !password) {
//             e.preventDefault(); // 폼 제출 막기

//             let emptyFields = [];
//             if (!userId) emptyFields.push("아이디");
//             if (!password) emptyFields.push("비밀번호");

//             const message = emptyFields.join(', ') + "을(를) 입력해 주세요.";
//             swal(message); // sweetalert 또는 alert(message)
//             return false;
//         }
//     });
// });

(function ($) {
 "use strict";

	$("body").on("click", "[data-ma-action]", function(e) {
        e.preventDefault();
        var $this = $(this),
            action = $(this).data("ma-action");
        switch (action) {
            case "nk-login-switch":
                var loginblock = $this.data("ma-block"),
                    loginParent = $this.closest(".nk-block");
                loginParent.removeClass("toggled"), setTimeout(function() {
                    $(loginblock).addClass("toggled")
                });
                break;
				case "print":
                window.print();
                break;
        }
    });

    $('#userUl li').on('click', function () {
        const selectedValue = $(this).data('value');
        const selectedText = $(this).text();
        
        $('#userType').val(selectedValue);
        
        $('.dropdown-trig-sgn button').text(selectedText);
    });


    

    
})(jQuery);






