from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..db import member_util
from ..models import User, db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method.lower() == 'get':
        return render_template("auth/login-register.html")

    userId = request.form.get('userId', '')
    password = request.form.get('password', '')
    chkRemember = request.form.get('chkRemember', 'off')

    # DB에서 사용자 정보를 가져옵니다.
    row = member_util.login(userId)
    if not row:
        return render_template("auth/login-register.html", message="잘못된 회원 정보입니다")

    # 비밀번호 확인
    if check_password_hash(row[4], password):  # 로그인 성공
        # User 객체로 로그인 처리
        user = User.query.get(userId)
        if not user:
            # DB에 User 객체가 없다면 직접 만들어도 되지만, 권장하지 않음.
            # member_util.login이 실제 DB 상태와 맞는지 확인 필요.
            return render_template("auth/login-register.html", message="사용자 정보를 찾을 수 없습니다.")

        login_user(user, remember=(chkRemember == 'on'))

        # flask_login 인증과 별개로 세션에 필요한 추가 정보 저장
        session['loginId'] = row[0]
        session['loginUserName'] = row[1]
        session['loginCompany'] = row[2]
        session['usertype'] = row[5]

        return redirect(url_for('main.index'))

    else:
        return render_template("auth/login-register.html", message="잘못된 회원 정보입니다")

@auth_bp.route('/logout', methods=['GET'])
def logout():
    logout_user()  # flask_login 로그아웃
    session.clear()  # 세션 정보 초기화
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['POST'])
def register():
    userId = request.form.get('userId')
    userName = request.form.get('userName')
    company = request.form.get('company')
    eMail = request.form.get('eMail')
    password = request.form.get('password')
    passwd_hash = generate_password_hash(password)
    usertype = request.form.get('userType')
    phone = request.form.get('phone')

    try:
        result = member_util.chk_id(userId)
        chk = 0 if result is None else int(result[0])
        if chk > 0:
            return render_template("auth/login-register.html", message="이미 등록된 아이디 입니다.")
        else:
            try:
                member_util.insert_member(userId, userName, company, eMail, passwd_hash, usertype, phone)
                return render_template("auth/login-register.html", message="가입 되었습니다.")
            except Exception as e:
                print(f"회원가입 에러: {e}")
                return render_template("auth/login-register.html", message="회원가입 중 오류가 발생했습니다. 관리자에게 문의하세요.")
    except Exception as e:
        print(f"회원가입 전체 에러 = {e}")
        return render_template("auth/login-register.html", message=f"{e} :::: 오류발생 관리자에게 문의하세요.")

@auth_bp.route("/chkId", methods=['GET'])
def chkId():
    userId = request.args.get('userId')
    try:
        result = member_util.chk_id(userId)
        idCnt = 0 if result is None else int(result[0])
        return jsonify({'success': True, 'idCnt': idCnt})
    except Exception as e:
        print(f"아이디 확인 에러: {e}")
        return jsonify({'success': False, 'message': '아이디 확인 중 오류가 발생했습니다. 관리자에게 문의하세요.'}), 500

@auth_bp.route("/myPage", methods=['GET', 'POST'])
def myPage():
    if request.method.lower() == 'get':
        loginId =  session.get('loginId')
        if loginId :
            try:
                row = member_util.selectMypage(loginId)
                return render_template("auth/myPage.html", row=row )
            except Exception as e:
                # print(f"아이디 확인 에러: {e}")
                return render_template("auth/myPage.html", message="잘못된 회원 정보입니다. 관리자에게 문의하세요.")
        else :
             return render_template("auth/login-register.html", message="회원 정보가 존재하지 않습니다.")
    else:
        userid = request.form.get('userid','')
        userName = request.form.get('userName','')
        userEmail = request.form.get('userEmail','')
        userPhone = request.form.get('userPhone','')
        userCompany = request.form.get('userCompany','')

        companyIntro = request.form.get('companyIntro','')
        ceoName = request.form.get('ceoName','')
        companyPhone = request.form.get('companyPhone','')
        companyFax = request.form.get('companyFax','')
        companyEmail = request.form.get('companyEmail','')
        companyHomepage = request.form.get('companyHomepage','')
        companyAddress = request.form.get('companyAddress','')
        companyAddressdetail = request.form.get('companyAddressdetail','')
        try:
            member_util.updateMypage(userid,userName,userEmail,userPhone,userCompany,companyIntro,ceoName,companyPhone,companyFax,companyEmail,companyHomepage,companyAddress,companyAddressdetail)
            return jsonify({"success": True, "message": "마이페이지가 수정 되었습니다."})
        except Exception as e:
            print(f"마이페이지 수정 에러: {e}")
            return jsonify({"success": False, "message": "마이페이지 수정 중 오류가 발생했습니다. 관리자에게 문의하세요."}), 500


@auth_bp.route("/delete", methods=['POST'])
def delete():
    userid = request.form.get('userid')
    result = member_util.chk_booking(userid)
    cnt = 0 if result is None else int(result[0])
    if cnt > 0 :
        return jsonify({"success": False, "cnt":cnt ,"message": "예약 신청 건이 있습니다. 취소 혹은 확정 후 탈퇴 해주세요."})
    else :
        try:
            member_util.deleteUser(userid)
            return jsonify({"success": True, "message": "회원 탈퇴 되었습니다."})
        except Exception as e:
            print(f"회원 탈퇴 에러: {e}")
            return jsonify({"success": False, "message": "회원 탈퇴 중 오류가 발생했습니다. 관리자에게 문의하세요."}), 500