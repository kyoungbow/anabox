$(document).ready(function () {
	const checkboxShipping = document.getElementById('checkbox-shipping');
	const checkboxPort = document.getElementById('checkbox-port');
	const dropdownShipping = document.getElementById('dropdown-shipping');
	const dropdownPort = document.getElementById('dropdown-port');

	// 공통 드롭다운 초기화 함수
	function resetDropdown($dropdown, placeholder) {
		$dropdown.empty();
		$dropdown.append(`<option value="">${placeholder}</option>`);
	}

	// 드롭다운 업데이트 함수
	function updateDropdowns() {
		const $dropdownShipping = $("#dropdown-shipping");
		const $dropdownPort = $("#dropdown-port");

		// 선사별 체크박스 처리
		if (checkboxShipping.checked) {
			dropdownShipping.style.display = 'block';

			$.ajax({
				url: "/stats/selectCompany",
				method: "GET",
				dataType: "json",
				success: function (data) {
					resetDropdown($dropdownShipping, "선사 전체");
					data.forEach(function (name) {
						$dropdownShipping.append(`<option value="${name}">${name}</option>`);
					});
				},
				error: function () {
					swal("선사 목록을 불러오는 데 실패했습니다.");
				}
			});
		} else {
			dropdownShipping.style.display = 'none';
			$dropdownShipping.val("");
		}

		// 항만별 체크박스 처리
		if (checkboxPort.checked) {
			dropdownPort.style.display = 'block';

			$.ajax({
				url: "/stats/selectLocation",
				method: "GET",
				dataType: "json",
				success: function (data) {
					resetDropdown($dropdownPort, "항만 전체");
					data.forEach(function (name) {
						$dropdownPort.append(`<option value="${name}">${name}</option>`);
					});
				},
				error: function () {
					swal("항만 목록을 불러오는 데 실패했습니다.");
				}
			});
		} else {
			dropdownPort.style.display = 'none';
			$dropdownPort.val("");
		}
	}

	// 이벤트 연결
	checkboxShipping.addEventListener('change', updateDropdowns);
	checkboxPort.addEventListener('change', updateDropdowns);

	// 초기 상태 설정
	updateDropdowns();

	$.ajax({
		url: "/stats/selectYears",
		method: "GET",
		dataType: "json",
		success: function (data) {
			const $dropdown = $("#year-dropdown");

			// 연도 옵션 추가
			data.forEach(function (year) {
				$dropdown.append(`<option value="${year}">${year}</option>`);
			});

			// 디폴트로 전년도 선택 (예: 2024년이면 2023 선택)
			const currentYear = new Date().getFullYear();
			const defaultYear = currentYear - 1;
			$dropdown.val(defaultYear.toString());
		},
		error: function (request) {
			swal("연도 목록을 불러오는 데 실패했습니다.");
		}
	});

	var company = $("#dropdown-shipping").val();
	var location = $("#dropdown-port").val();
	var year = $("#year-dropdown").val();

	$("#btnStats").on("click", function () {

		company = $("#dropdown-shipping").val();
		location = $("#dropdown-port").val();
		year = $("#year-dropdown").val();
		viewChart(year, company, location);
	});

	function viewChart(year, company, location) {
		// const year = $("#year-dropdown").val();  // ✅ 드롭다운에서 선택된 연도 가져오기

		$.ajax({
			url: "/stats/selectChartData",
			method: "POST",
			data: {
				"year": year,
				"company": company,
				"location": location
			},
			dataType: "json",
			success: function (data) {
				if (!data.success) {
					swal(data.message || "데이터 조회 실패");
					return;
				}
				const rows = data.data;

				const labels = Array.from({ length: 12 }, (_, i) => `${year}-${String(i + 1).padStart(2, '0')}`);
				const supply = Array(12).fill(0);
				const requested = Array(12).fill(0);
				const confirmed = Array(12).fill(0);
				const pending = Array(12).fill(0);
				const unbooked = Array(12).fill(0);

				rows.forEach(item => {
					const date = new Date(item.year_month);
					const monthIndex = date.getMonth();

					supply[monthIndex] += item.supply_count;
					requested[monthIndex] += item.requested_bookings;
					confirmed[monthIndex] += item.confirmed_bookings;
					pending[monthIndex] += item.pending_bookings;
					unbooked[monthIndex] += item.unbooked_supply;
				});

				const ctx = document.getElementById('myChart').getContext('2d');

				if (window.myChart && typeof window.myChart.destroy === 'function') {
					window.myChart.destroy();
				}

				window.myChart = new Chart(ctx, {
					type: 'bar',
					data: {
						labels: labels,
						datasets: [
							{ label: '등록', data: supply, backgroundColor: 'rgba(75, 192, 192, 0.7)' },
							{ label: '예약 신청', data: requested, backgroundColor: 'rgba(54, 162, 235, 0.7)' },
							{ label: '예약 확정', data: confirmed, backgroundColor: 'rgba(255, 206, 86, 0.7)' },
							{ label: '예약 미확정', data: pending, backgroundColor: 'rgba(255, 99, 132, 0.7)' },
							{ label: '예약 없음', data: unbooked, backgroundColor: 'rgba(153, 102, 255, 0.7)' }
						]
					},
					options: {
						responsive: true,
						plugins: {
							title: {
								display: true,
								text: `${year}년 월별 공급 vs 수급`
							}
						},
						scales: {
							x: { stacked: false },
							y: { beginAtZero: true }
						}
					}
				});
			},
			error: function (request) {
				const message = request.responseJSON?.message || "서버 요청 중 오류가 발생했습니다.";
				swal(message);
			}
		});

	}

	viewChart(2024, company, location);

});
