

$(document).ready(function () {

    const blockAllKeyboardFields = ['availableFrom', 'availableTo'];
    const today = new Date();
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(today.getDate() + 7);

    // yyyy-mm-dd 형식으로 포맷
    const formatDate = (date) => {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, "0");
        const day = String(date.getDate()).padStart(2, "0");
        return `${year}-${month}-${day}`;
    };

    $("#availableFrom").val(formatDate(today));
    $("#availableTo").val(formatDate(sevenDaysAgo));

    var form = $('#bookingListForm');
    var formData = form.serialize();

    // 날짜 필드 키보드 입력 완전 차단 (availableFrom, availableTo)
    blockAllKeyboardFields.forEach(id => {
        const input = document.getElementById(id);
        if (!input) return;
        input.addEventListener("keydown", function(e) {
            e.preventDefault();
        });
    });

    function formatKoreanDate(dateStr) {
        const date = new Date(dateStr);
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0'); // 1월은 0
        const day = String(date.getDate()).padStart(2, '0');

        return `${year}년 ${month}월 ${day}일`;
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

    function bookingList() {
        $.ajax({
            url: "/container/bookingListAjax",
            method: "GET",
            data: formData,
            dataType: "json",
            success: function (data) {
                // DataTable이 이미 초기화되어 있으면 재사용
                const table = $("#data-table-basic").DataTable();

                // 기존 이벤트 제거 방지 위해 off()
                $('#data-table-basic tbody').off('click', 'tr');

                // 데이터 포맷
                const formattedData = data.map(row => {
                    return {
                        regNum: row[0], // 클릭 이동에 사용할 ID
                        rowData: [
                            row[2],
                            row[3],
                            Number(row[4]).toLocaleString(),
                            row[5],
                            row[6],
                            row[7],
                            formatKoreanDate(row[8]),
                            formatKoreanDate(row[9]),
                            Number(row[11]).toLocaleString(),
                            row[13]
                        ]
                    };
                });

                // 테이블 초기화 후 데이터 설정
                table.clear();
                formattedData.forEach(item => {
                    table.row.add(item.rowData);
                });
                table.draw();

                // 각 tr 클릭 시 row[1]을 기반으로 페이지 이동
                $('#data-table-basic tbody').on('click', 'tr', function () {
                    const rowIndex = table.row(this).index();
                    const regNum = formattedData[rowIndex]?.regNum;

                    if (regNum) {
                        postToDetail(regNum);
                    }
                });
            },
            error: function (request) {
                const message = request.responseJSON?.message || "서버 요청 중 오류가 발생했습니다!";
                swal(message);
            }
        });
    }

    bookingList();

    $('#btnSearch').on('click', function(e) {
        e.preventDefault();  // 폼 기본 제출 막기

        var userId = $('#userId').val().trim()
        var availableFrom = $('#availableFrom').val().trim()
        var availableTo = $('#availableTo').val().trim()

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
        var formData = form.serialize();
        $.ajax({
            url: "/container/bookingListAjax",
            method: "GET",
            data: formData,
            dataType: "json",
            success: function (data) {
                // DataTable이 이미 초기화되어 있으면 재사용
                const table = $("#data-table-basic").DataTable();

                // 기존 이벤트 제거 방지 위해 off()
                $('#data-table-basic tbody').off('click', 'tr');

                // 데이터 포맷
                const formattedData = data.map(row => {
                    return {
                        regNum: row[0], // 클릭 이동에 사용할 ID
                        rowData: [
                            row[2],
                            row[3],
                            Number(row[4]).toLocaleString(),
                            row[5],
                            row[6],
                            row[7],
                            formatKoreanDate(row[8]),
                            formatKoreanDate(row[9]),
                            Number(row[11]).toLocaleString(),
                            row[13]
                        ]
                    };
                });

                // 테이블 초기화 후 데이터 설정
                table.clear();
                formattedData.forEach(item => {
                    table.row.add(item.rowData);
                });
                table.draw();

                // 각 tr 클릭 시 row[1]을 기반으로 페이지 이동
                $('#data-table-basic tbody').on('click', 'tr', function () {
                    const rowIndex = table.row(this).index();
                    const regNum = formattedData[rowIndex]?.regNum;

                    if (regNum) {
                        postToDetail(regNum);
                    }
                });
            },
            error: function (request) {
                const message = request.responseJSON?.message || "서버 요청 중 오류가 발생했습니다!";
                swal(message);
            }
        });
    });
});









