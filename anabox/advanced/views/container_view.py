from flask import Blueprint,render_template,request,jsonify, session
import json
from ..db import container_util
from datetime import datetime
import pandas as pd

container_bp = Blueprint("container", __name__, url_prefix=
                    "/container")

# 컨테이너 등록
@container_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method.lower() == 'get':
        return render_template("container/register.html")
    else:
        userId = request.form.get('userId')
        containerNumber = request.form.get('containerNumber')
        size = request.form.get('size')
        tareWeight = request.form.get('tareWeight').replace(",","")
        terminal = request.form.get('terminal')
        location = request.form.get('location')
        portType = request.form.get('portType')
        availableFrom = request.form.get('availableFrom')
        availableTo = request.form.get('availableTo')
        rentalDays = (datetime.strptime(availableTo, "%Y-%m-%d") - datetime.strptime(availableFrom, "%Y-%m-%d")).days + 1
        pricePerDay = request.form.get('pricePerDay').replace(",","")
        totalPrice = int(pricePerDay) * rentalDays
        remarks = request.form.get('remarks')
        try:
            container_util.register(userId,containerNumber,size,tareWeight,terminal,location,portType,availableFrom,availableTo,rentalDays,pricePerDay,totalPrice,remarks)
            return jsonify({"success": True, "message": "컨테이너가 등록 되었습니다."})
        except Exception as e:
            # 로깅 추천
            print(f"컨테이너 등록 실패: {e}")
            return jsonify({"success": False, "message": "컨테이너 등록 중 오류가 발생했습니다. 관리자에게 문의하세요."}), 500

# 컨테이너 리스트 조회
@container_bp.route("/containerList", methods=['GET'])
def containerList():
    return render_template("container/containerList.html")

# 컨테이너 리스트 조회(ajax)
@container_bp.route("/containerListAjax", methods=['GET'])
def containerListAjax():

    userId = request.args.get('userId')
    availableFrom = request.args.get('availableFrom')
    availableTo = request.args.get('availableTo')
    userType = request.args.get('usertype')
    route = request.args.get('route', "None")
    rows = container_util.selectContainerList(userId,availableFrom,availableTo,userType,route)

    return jsonify(rows)


# 컨테이너 상세 조회
@container_bp.route("/containerDetail", methods=['GET', 'POST'])
def containerDetail():
    if request.method == 'POST':
        param = request.form.get('param')
    else:
        param = request.args.get('param')
    try:
        row = container_util.selectContainerDetail(param)
        return render_template("container/detail.html",row=row)
    except Exception as e:
        # 로깅 추천
        print(f"컨테이너 디테일 조회 실패: {e}")
        return render_template("container/detail.html", message= "컨테이너 조회 중 오류가 발생했습니다. 관리자에게 문의하세요.")

# 컨테이너 삭제
@container_bp.route("/delete", methods=['POST'])
def delete():
    regNum = request.form.get('regNum')
    userId = request.form.get('userId')

    try:
        container_util.delete(regNum,userId)
        return jsonify({"success": True, "message": "컨테이너가 삭제 되었습니다."})
    except Exception as e:
        # 로깅 추천
        print(f"컨테이너 삭제 실패: {e}")
        return jsonify({"success": False, "message": "컨테이너 삭제 중 오류가 발생했습니다. 관리자에게 문의하세요."})

# 컨테이너 수정
@container_bp.route("/update", methods=['POST'])
def update():
        regNum = request.form.get('regNum')
        userId = request.form.get('userId')
        containerNumber = request.form.get('containerNumber')
        size = request.form.get('size')
        tareWeight = request.form.get('tareWeight').replace(",","")
        terminal = request.form.get('terminal')
        location = request.form.get('location')
        portType = request.form.get('portType')
        availableFrom = request.form.get('availableFrom')
        availableTo = request.form.get('availableTo')
        rentalDays = (datetime.strptime(availableTo, "%Y-%m-%d") - datetime.strptime(availableFrom, "%Y-%m-%d")).days + 1
        pricePerDay = request.form.get('pricePerDay').replace(",","")
        totalPrice = int(pricePerDay) * rentalDays
        remarks = request.form.get('remarks')
        try:
            container_util.update(regNum,userId,containerNumber,size,tareWeight,terminal,location,portType,availableFrom,availableTo,rentalDays,pricePerDay,totalPrice,remarks)
            return jsonify({"success": True, "message": "컨테이너가 수정 되었습니다."})
        except Exception as e:
            # 로깅 추천
            print(f"컨테이너 수정 실패: {e}")
            return jsonify({"success": False, "message": "컨테이너 수정 중 오류가 발생했습니다. 관리자에게 문의하세요."}), 500
        
# 예약리스트 조회
@container_bp.route("/bookingList", methods=['GET'])
def bookingList():
    return render_template("container/bookingList.html")

# 예약리스트 조회(ajax)
@container_bp.route("/bookingListAjax", methods=['GET'])
def bookingListAjax():

    userId = request.args.get('userId')
    availableFrom = request.args.get('availableFrom')
    availableTo = request.args.get('availableTo')
    bookingStatus = request.args.get('bookingStatus')
    usertype = request.args.get('usertype')
    
    rows = container_util.selectBookingList(userId,availableFrom,availableTo,bookingStatus,usertype)

    return jsonify(rows)

# 예약 상세 조회
@container_bp.route("/bookingDetail", methods=['GET', 'POST'])
def bookingDetail():
    if request.method == 'POST':
        param = request.form.get('param')
    else:
        param = request.args.get('param')
    try:
        row = container_util.selectBookingDetail(param)
        return render_template("container/bookingDetail.html",row=row)
    except Exception as e:
        # 로깅 추천
        print(f"컨테이너 디테일 조회 실패: {e}")
        return render_template("container/bookingDetail.html", message= "예약 상세 조회 중 오류가 발생했습니다. 관리자에게 문의하세요.")
    

# 예약 취소
@container_bp.route("/bookingCancel", methods=['POST'])
def bookingCancel():
    bookingNum = request.form.get('bookingNum')
    regNum = request.form.get('regNum')

    try:
        container_util.bookingCancel(bookingNum,regNum)
        container_util.deleteMessenger(bookingNum)
        return jsonify({"success": True, "message": "예약이 취소 되었습니다."})
    except Exception as e:
        # 로깅 추천
        print(f"예약 취소 실패: {e}")
        return jsonify({"success": False, "message": "예약 취소 중 오류가 발생했습니다. 관리자에게 문의하세요."})
    
# 예약 확정
@container_bp.route("/booking", methods=['POST'])
def booking():
    bookingNum = request.form.get('bookingNum')
    regNum = request.form.get('regNum')

    try:
        container_util.booking(bookingNum,regNum)
        return jsonify({"success": True, "message": "예약이 확정 되었습니다."})
    except Exception as e:
        # 로깅 추천
        print(f"예약 확정 실패: {e}")
        return jsonify({"success": False, "message": "예약 확정 중 오류가 발생했습니다. 관리자에게 문의하세요."})
    
# 예약확정 취소
@container_bp.route("/bookingConfirmCancel", methods=['POST'])
def bookingConfirmCancel():
    bookingNum = request.form.get('bookingNum')
    regNum = request.form.get('regNum')

    try:
        container_util.bookingConfirmCancel(bookingNum,regNum)
        return jsonify({"success": True, "message": "예약 확정이 취소 되었습니다."})
    except Exception as e:
        # 로깅 추천
        print(f"예약 확정 취소 실패: {e}")
        return jsonify({"success": False, "message": "예약 확정 취소 중 오류가 발생했습니다. 관리자에게 문의하세요."})
    
# 예약 신청
@container_bp.route("/bookingApply", methods=['POST'])
def bookingApply():
    regNum = request.form.get('regNum')
    userId = request.form.get('userId')
    registerId = request.form.get('registerId')
    try:
        container_util.bookingApply(regNum,userId,registerId)
        # 예약번호 조회
        bookingNum = container_util.selectBookingNum(regNum,userId,registerId)
        # 예약번호 조회 후 채팅방 생성
        container_util.createMessenger(bookingNum,userId,registerId)
        return jsonify({"success": True, "message": "예약 신청 되었습니다."})
    except Exception as e:
        # 로깅 추천
        print(f"예약 신청 실패: {e}")
        return jsonify({"success": False, "message": "예약 신청 중 오류가 발생했습니다. 관리자에게 문의하세요."})
    
# 컨테이너 대량 등록
@container_bp.route("/bulkRegister", methods=['GET', 'POST'])
def bulkRegister():
    if request.method.lower() == 'get':
        return render_template("container/bulkRegister.html")
    else:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "잘못된 요청입니다."}), 400
        
        userId = data.get('userId')
        dataList = data.get('dataList')

        try:
            # 여기에 실제 처리 로직 추가
            container_util.bulkRegister(userId,dataList)
            return jsonify({"success": True, "message": "컨테이너가 대량 등록 되었습니다."})
        except Exception as e:
            print(f"컨테이너 대량 등록 실패: {e}")
            return jsonify({"success": False, "message": "컨테이너 대량 등록 중 오류가 발생했습니다."}), 500

# 엑셀 유효성 검사

REQUIRED_COLUMNS = [
    'containerNumber', 'size', 'tareWeight', 'terminal',
    'location', 'portType', 'availableFrom', 'availableTo',
    'pricePerDay', 'remarks'  # remarks는 선택 필드지만 컬럼은 있어야 함
]

def validate_excel(df):
    errors = []

    # 컬럼 검사
    if list(df.columns) != REQUIRED_COLUMNS:
        return [f"엑셀 컬럼이 정확히 다음과 같아야 합니다: {', '.join(REQUIRED_COLUMNS)}"]
    
    # 데이터 행이 하나도 없으면 오류
    if df.empty:
        errors.append("엑셀 파일에 데이터가 하나도 없습니다. 엑셀 파일에 데이터를 입력하세요.")
        return errors
    
    # 행별 유효성
    for i, row in df.iterrows():
        row_num = i + 2  # 헤더는 1행
        # 필수 필드 누락 검사
        
        for col in REQUIRED_COLUMNS:
            val = row[col]
            print(f"행{col}== {val}")
            if col != 'remarks' and (pd.isna(val) or str(val).strip() == ''):
                errors.append(f"{row_num}행: '{col}' 값이 비어 있습니다.")

        # 숫자형 필드 검사
        for num_col in ['tareWeight', 'pricePerDay']:
            try:
                int(row[num_col])
            except:
                errors.append(f"{row_num}행: '{num_col}'은 정수여야 합니다.")

        # 날짜형 필드 검사
        for date_col in ['availableFrom', 'availableTo']:
            try:
                pd.to_datetime(row[date_col])
            except:
                errors.append(f"{row_num}행: '{date_col}' 날짜 형식 오류")

    return errors


@container_bp.route('/upload', methods=['POST'])
def upload():
    ALLOWED_EXTENSIONS = {'xls', 'xlsx'}
    
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    file = request.files.get('file')

    if not file or file.filename == '':
        return jsonify({'error': '파일이 제공되지 않았습니다.'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': '엑셀 파일만 업로드할 수 있습니다.'}), 400

    try:
        df = pd.read_excel(file)
        df = df.iloc[:, :10]
        df = df.drop(index=0).reset_index(drop=True)
        print(df)
        # 유효성 검사
        validation_errors = validate_excel(df)

        if validation_errors:
            return jsonify({'error': f"{validation_errors}"}), 400

        # 렌탈일수 및 총 가격 계산
        df['rentalDays'] = (pd.to_datetime(df['availableTo']) - pd.to_datetime(df['availableFrom'])).dt.days + 1
        df['totalPrice'] = df['rentalDays'] * df['pricePerDay']

        df['availableFrom'] = pd.to_datetime(df['availableFrom']).dt.strftime('%Y-%m-%d')
        df['availableTo'] = pd.to_datetime(df['availableTo']).dt.strftime('%Y-%m-%d')

        # 컬럼 순서 유지 미리보기 (상위 5개만)
        preview_json = df[REQUIRED_COLUMNS + ['rentalDays', 'totalPrice']].to_json(orient='records', force_ascii=False)
        preview = json.loads(preview_json)
        print(preview)
        return jsonify({
            'success': '엑셀 업로드를 성공했습니다.',
            'preview': preview
        }), 200

    except Exception as e:
        return jsonify({'error': f'엑셀 처리 실패: {str(e)}'}), 500
