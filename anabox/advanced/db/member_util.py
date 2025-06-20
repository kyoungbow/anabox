import psycopg2
from . import dbInfo
## 중복 아이디 체크

def chk_id(userId):
    conn = None
    cursor = None
    row = None
    try:
        conn = dbInfo.dbConn()
        cursor = conn.cursor()
        sql = "select count(*) from tbl_users where id = %s"
        cursor.execute(sql, (userId,))  # <-- 튜플로 전달
        row = cursor.fetchone()
    except Exception as e:
        print(f"오류발생 = {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return row

## 회원가입

def insert_member(id, userName, company, eMail, passwd, usertype, phone):
    conn = None
    cursor = None
    try:
        conn =  dbInfo.dbConn()
        cursor = conn.cursor()
        sql = "insert into tbl_users (id, username, company, email, password, usertype, phone ) values (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql,(id, userName, company, eMail, passwd, usertype, phone))
        conn.commit()
    except Exception as e :
        print(f"회원가입 오류발생 == {e}")
        if conn: # DML 구문에서는 넣어줘야 함
            conn.rollback()
        raise
    finally:
        if cursor :
            cursor.close()
        if conn :
            conn.close()

## 로그인

def login(userId):
    conn = None
    cursor = None
    row = None
    try:
        conn =  dbInfo.dbConn()

        cursor = conn.cursor()
        sql = """select 
                    id, username, company, email, password, usertype 
                from tbl_users 
                where id = %s """
        cursor.execute(sql,(userId,))
        row =  cursor.fetchone()

    except Exception as e :
        print(f"오류발생 = {e}")
        if conn: # DML 구문에서는 넣어줘야 함
            conn.rollback()
    finally:
        if cursor :
            cursor.close()
        if conn :
            conn.close()
    return row


def selectMypage(userId):
    conn = None
    cursor = None
    row = None
    try:
        conn =  dbInfo.dbConn()

        cursor = conn.cursor()
        sql = """
                select 
                    a.*,
                    b.*
                from tbl_users a
                LEFT JOIN
                tbl_company b ON a.id = b.id
                where a.id = %s
                """
        cursor.execute(sql,(userId,))
        row =  cursor.fetchone()

    except Exception as e :
        print(f"마이페이지 조회 오류발생 = {e}")
        if conn: # DML 구문에서는 넣어줘야 함
            conn.rollback()
    finally:
        if cursor :
            cursor.close()
        if conn :
            conn.close()
    
    return row

def updateMypage(userid,userName,userEmail,userPhone,userCompany,
                 companyIntro,ceoName,companyPhone,companyFax,companyEmail,companyHomepage,
                 companyAddress,companyAddressdetail):
    conn = None
    cursor = None
    try:
        conn =  dbInfo.dbConn()
        cursor = conn.cursor()

        sql = """
                    UPDATE tbl_users
                    SET
                        username = %s,
                        company = %s,
                        email = %s,
                        phone = %s
                    WHERE
                        id = %s
                """
        cursor.execute(sql,(userName,userCompany,userEmail,userPhone, userid))

        sql = """
                INSERT INTO tbl_company (
                    id,
                    companyname,
                    companyintro,
                    ceoname,
                    phone,
                    fax,
                    email,
                    homepage,
                    address,
                    addressdetail
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE
                SET 
                    companyname = EXCLUDED.companyname,
                    companyintro = EXCLUDED.companyintro,
                    ceoname = EXCLUDED.ceoname,
                    phone = EXCLUDED.phone,
                    fax = EXCLUDED.fax,
                    email = EXCLUDED.email,
                    homepage = EXCLUDED.homepage,
                    address = EXCLUDED.address,
                    addressdetail = EXCLUDED.addressdetail
            """
        cursor.execute(sql,(userid,userCompany,companyIntro,ceoName,companyPhone,companyFax,companyEmail,companyHomepage,
                 companyAddress,companyAddressdetail))

        conn.commit()
    except Exception as e :
        print(f"마이페이지 수정 오류 == {e}")
        if conn: # DML 구문에서는 넣어줘야 함
            conn.rollback()
        raise
    finally:
        if cursor :
            cursor.close()
        if conn :
            conn.close()

def chk_booking(userId):
    conn = None
    cursor = None
    row = None
    try:
        conn = dbInfo.dbConn()
        cursor = conn.cursor()
        sql = """
                select 
                    count(*) 
                from tbl_booking
                where (rentalid = %s or registerid = %s) 
                and bookingstatus = 'N'
            """
        cursor.execute(sql, (userId,userId))  # <-- 튜플로 전달
        row = cursor.fetchone()
    except Exception as e:
        print(f"오류발생 = {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return row


def deleteUser(userid):
    conn = None
    cursor = None
    try:
        conn = dbInfo.dbConn()
        cursor = conn.cursor()

        sql = "DELETE FROM tbl_message WHERE sendid = %s"
        cursor.execute(sql, (userid,))

        sql = "DELETE FROM tbl_messenger WHERE id1 = %s OR id2 = %s"
        cursor.execute(sql, (userid, userid))

        sql = "DELETE FROM tbl_booking WHERE rentalid = %s OR registerid = %s"
        cursor.execute(sql, (userid, userid))

        sql = "DELETE FROM tbl_container WHERE id = %s"
        cursor.execute(sql, (userid,))

        sql = "DELETE FROM tbl_users WHERE id = %s"
        cursor.execute(sql, (userid,))

        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"회원 삭제 중 오류 발생: {e}")
        raise
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
            