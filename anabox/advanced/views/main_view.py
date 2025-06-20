
from flask import Blueprint,render_template,request, session,jsonify
from ..db import main_util

main_bp = Blueprint('main', __name__, url_prefix="/")

@main_bp.route("/", methods=['GET'])
def index():
    # 요청 데이터 읽기
    # 요청 처리
    # 응답 컨텐츠 생산

    id =  session.get('loginId')
    usertype = session.get('usertype')

    rows = main_util.selectMydata(id, usertype)

    return render_template('index.html',rows=rows)


# 예약 신청 조회(ajax)
@main_bp.route("/recentBookingApply", methods=['GET'])
def recentBookingApply():
    row = main_util.recentBookingApply()
    return jsonify(row)


# 헤더 예약 카운트 (ajax)
@main_bp.route("/applyCnt", methods=['GET'])
def applyCnt():
    userId = request.args.get('userId')
    usertype = request.args.get('usertype')
    cnt = main_util.headerApplyCnt(userId,usertype)
    return jsonify({'cnt': cnt})

# 헤더 메신저 카운트 (ajax)
@main_bp.route("/messengerCnt", methods=['GET'])
def messengerCnt():
    userId = request.args.get('userId')
    cnt = main_util.headerMessengerCnt(userId)
    return jsonify({'cnt': cnt})

# 헤더 예약 리스트 (ajax)
@main_bp.route("/applyList", methods=['GET'])
def applyList():
    userId = request.args.get('userId')
    usertype = request.args.get('usertype')
    rows = main_util.headerApplyList(userId,usertype)
    return jsonify(rows)

# 헤더 메신저 리스트 (ajax)
@main_bp.route("/messengerList", methods=['GET'])
def messengerList():
    userId = request.args.get('userId')
    rows = main_util.headerMessengerList(userId)
    return jsonify(rows)



