$(document).ready(function () {
    const form = $('#bookingDetailForm');
    const formData = form.serialize();

   
    // 뒤로
    $('#btnBack').on('click', function(e) {
        history.back();
    });

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

    $('#btnBookerCompany').on('click', function(e) {
        var ownerId = $("#ownerId").val().trim();
        postToCompany(ownerId);
    });
    $('#btnRegisterCompany').on('click', function(e) {
        var partnerId = $("#partnerId").val().trim();
        postToCompany(partnerId);
    });


    $('#btnCancel').on('click', function(e) {
        swal({   
			title: "컨테이너 예약 취소",   
			text: "예약을 취소 하시겠습니까?",   
			type: "warning",   
			showCancelButton: true,   
			confirmButtonText: "예",
            cancelButtonText: "아니요",
		}).then(function(){
            
            $.ajax({
                url: "/container/bookingCancel",
                method: "POST",
                data: formData,
                dataType: "json",
                success: function (data) {
                    swal("예약 취소", data.message, "success")
                    .then(function() {
                        window.location.href = "/container/bookingList";  
                    });
                },
                error: function (request) {
                    const message = request.responseJSON?.message || "서버 요청 중 오류가 발생했습니다!";
                    swal(message);
                }
            });
        });
    });

    $('#btnBooking').on('click', function(e) {
        swal({   
			title: "컨테이너 예약 확정",   
			text: "예약을 확정 하시겠습니까?",   
			type: "warning",   
			showCancelButton: true,   
			confirmButtonText: "예",
            cancelButtonText: "아니요",
		}).then(function(){
            
            $.ajax({
                url: "/container/booking",
                method: "POST",
                data: formData,
                dataType: "json",
                success: function (data) {
                    swal("예약 확정", data.message, "success")
                    .then(function() {
                        window.location.href = "/container/bookingList";  
                    });
                },
                error: function (request) {
                    const message = request.responseJSON?.message || "서버 요청 중 오류가 발생했습니다!";
                    swal(message);
                }
            });
        });
    });
    

    $('#btnBookingCancel').on('click', function(e) {
        swal({   
			title: "컨테이너 예약 확정 취소",
			text: "확정된 예약을 예약 중으로 변경 하시겠습니까?",   
			type: "warning",   
			showCancelButton: true,   
			confirmButtonText: "예",
            cancelButtonText: "아니요",
		}).then(function(){
            var regNum = $("#regNum").val();
            $.ajax({
                url: "/container/bookingConfirmCancel",
                method: "POST",
                data: formData,
                dataType: "json",
                success: function (data) {
                    swal("예약 확정 취소", data.message, "success")
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
    

});









