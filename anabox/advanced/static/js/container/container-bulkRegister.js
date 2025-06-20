

$(document).ready(function () {
    let trhtml = ""

    function renderPreview(data) {
        const orderedKeys = [
            'containerNumber',
            'size',
            'tareWeight',
            'terminal',
            'location',
            'portType',
            'availableFrom',
            'availableTo',
            'rentalDays',
            'pricePerDay',
            'totalPrice',
            'remarks'
        ];

        
        let html = "<div class='view-mail-hrd' id='registerList'><h2>등록 리스트</h2></div> <table class='table preview'><thead><tr>";
        orderedKeys.forEach(key => {
            html += `<th>${key}</th>`;
        });
        html += "</tr></thead><tbody>";
        data.forEach(row => {
            trhtml += "<tr>";
            orderedKeys.forEach(key => {
                trhtml += `<td name="${key}">${row[key] !== undefined ? row[key] : ''}</td>`;
            });
            trhtml += "</tr>";
        });
        html += trhtml;
        html += "</tbody></table>";
        $("#preview-container").html(html);
    }
    
    Dropzone.options.demoUpload = {
        paramName: "file", 
        maxFilesize: 5, 
        init: function () {
            this.on("success", function (file, response) {
                if (response.preview) {
                    // console.log("미리보기 데이터", response.preview);
                    swal("파일 업로드", response.success, "success");
                    // 사용자에게 테이블 등으로 표시할 수 있음
                    renderPreview(response.preview);
                } else if (response.error) {
                    swal("파일 업로드 실패", response.error, "error");
                }
            });
            this.on("error", function (file, response) {
                swal("파일 업로드 실패", response.error, "error");
            });
        }
    };

    $(document).on("click", ".dz-error.dz-complete", function() {
        $(this).remove();
        if ($('.dz-message.needsclick.download-custom').siblings().length === 0) {
            $("#demo-upload")
            .removeClass() // 기존 클래스 전체 제거
            .addClass("dropzone dropzone-custom needsclick dz-clickable");
            // 원하는 동작 수행
        }
    });
    
    $("#btnDonwLoad").click(function(){
        swal({   
			title: "파일 다운로드",   
			text: "대량 등록 Excel파일을 다운로드 받으시겠습니까?",   
			type: "info",   
			showCancelButton: true,   
			confirmButtonText: "예",
            cancelButtonText: "아니요",
		}).then(function(){
            const link = document.createElement('a');
            link.href = '/static/containerSample.xlsx';  // 파일 경로
            link.download = 'containerSample.xlsx';        // 저장될 파일 이름 (optional)
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
    });

    $("#btnFileRemove").click(function(){
        if ($('.dz-message.needsclick.download-custom').siblings().length === 0) {
            swal("파일 초기화", "업로드 된 파일이 없습니다.", "error");
            return false;
        }
        swal({   
			title: "파일 초기화",   
			text: "업로드 된 파일을 초기화 하시겠습니까?",   
			type: "warning",   
			showCancelButton: true,   
			confirmButtonText: "예",
            cancelButtonText: "아니요",
		}).then(function(){
            trhtml = ""
            $("#registerList").remove();
            $(".table.preview").remove();
            $(".dz-complete").remove();
            $("#demo-upload")
            .removeClass() // 기존 클래스 전체 제거
            .addClass("dropzone dropzone-custom needsclick dz-clickable");
            swal("파일 초기화", "파일을 초기화 했습니다. 다시 업로드 해주세요.", "success");
        });
    });

    $("#btnBulkRegister").click(function(){
        if ($("#preview-container").children().length < 1) {
            swal("대량 등록", "등록 가능한 파일이 없습니다.", "error");
            return false;
        }

        swal({   
			title: "대량 등록",   
			text: "대량 등록 하시겠습니까?",   
			type: "warning",   
			showCancelButton: true,   
			confirmButtonText: "예",
            cancelButtonText: "아니요",
		}).then(function(){
            const rows = document.querySelectorAll("tbody tr");
            const dataList = [];
            var userId = $("#userId").val();
            rows.forEach(tr => {
                const rowData = {};
                tr.querySelectorAll("td").forEach(td => {
                    const key = td.getAttribute("name");
                    const value = td.innerText.trim();
                    rowData[key] = value;
                });
                dataList.push(rowData);
            });

            // console.log(dataList);

            $.ajax({
                "url": "/container/bulkRegister",
                "method": "POST",
                contentType: "application/json",  // JSON 형식 명시
                data: JSON.stringify({userId: userId, dataList: dataList}),  // JSON 문자열로 변환
                dataType: "json",
                "success": function(data, status, xhr) {
                    const message = data.message;

                    swal("대량 등록", message, "success")
                    .then(function() {
                        window.location.href = "/container/containerList"; 
                    });
                },
                "error": function(request) {
                    const message = request.responseJSON?.message || "서버 요청 중 오류가 발생했습니다!.";
                    swal(message);
                }
            });
        });
    });
        

});







