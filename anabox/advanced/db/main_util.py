import psycopg2
from . import dbInfo

## 인덱스 마이 데이터 조회
def selectMydata(id, usertype):
    conn = None
    cursor = None
    rows = None
    try:
        conn = dbInfo.dbConn()
        cursor = conn.cursor()
        if usertype == 1 :
            sql = """
                    select 
                        count(*),
                        (
                            select 
                                count(*) 
                            from tbl_container
                            where regdate = CURRENT_DATE
                        ),
                        (
                            select 
                                count(*) 
                            from tbl_container
                            where id = %s
                        ),
                        (
                            select 
                                COALESCE(sum(totalprice), 0)
                            from tbl_container a
                            LEFT JOIN
                                tbl_booking b ON a.regnum = b.regnum
                            where a.id = %s
                            AND b.bookingstatus = 'Y'
                        )
                    from tbl_container
                    """
        else :
            sql = """
                    select 
                        count(*),
                        (
                            select 
                                count(*) 
                            from tbl_container
                            where regdate = CURRENT_DATE
                        ),
                        (
                            select 
                                count(*)
                            from tbl_container a
                            LEFT JOIN
                                tbl_booking b ON a.regnum = b.regnum
                            where b.rentalid = %s
                            AND b.bookingstatus = 'Y'
                        ),
                        (
                            select 
                                COALESCE(sum(totalprice), 0)
                            from tbl_container a
                            LEFT JOIN
                                tbl_booking b ON a.regnum = b.regnum
                            where b.rentalid = %s
                            AND b.bookingstatus = 'Y'
                        )
                    from tbl_container
            """
        cursor.execute(sql, (id,id))  # <-- 튜플로 전달
        rows = cursor.fetchall()
    except Exception as e:
        print(f"메인페이지 마이 데이터 조회 오류 = {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows

def recentBookingApply():
    conn = None
    cursor = None
    rows = None
    try:
        conn = dbInfo.dbConn()
        cursor = conn.cursor()
        sql = """
                select 
                    a.terminal,
                    a.containernumber,
                    a.totalprice
                from tbl_container a
                LEFT JOIN
                    tbl_booking b ON a.regnum = b.regnum
                where b.bookingstatus = 'N'
                order by b.bookingdate desc
                limit 10
            """
        cursor.execute(sql)  # <-- 튜플로 전달
        rows = cursor.fetchall()
    except Exception as e:
        print(f"메인페이지 최근 예약 근황 조회 오류 = {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows

def headerApplyCnt(id,usertype):
    conn = None
    cursor = None
    rows = None
    try:
        conn = dbInfo.dbConn()
        cursor = conn.cursor()
        if usertype == "1":
            sql = """
                    SELECT
                        count(*)
                    FROM
                    tbl_container c
                    LEFT JOIN
                    tbl_booking b ON c.regnum = b.regnum
                    WHERE
                    c.id = %s
                    and b.bookingstatus ='N'
                """
        else:
            sql = """
                    SELECT
                        count(*)
                    FROM
                    tbl_container c
                    LEFT JOIN
                    tbl_booking b ON c.regnum = b.regnum
                    WHERE
                    b.rentalid = %s
                    and b.bookingstatus ='Y'
                """
        cursor.execute(sql, (id,))  # <-- 튜플로 전달
        rows = cursor.fetchall()
    except Exception as e:
        print(f"헤더 신청 카운트 조회 실패 = {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows

def headerMessengerCnt(id):
    conn = None
    cursor = None
    rows = None
    try:
        conn = dbInfo.dbConn()
        cursor = conn.cursor()
        sql = """
                SELECT
                    count(*)
                FROM
                tbl_messenger
                where id1 = %s
                or id2 = %s
            """
        cursor.execute(sql, (id,id))  # <-- 튜플로 전달
        rows = cursor.fetchall()
    except Exception as e:
        print(f"헤더 신청 카운트 조회 실패 = {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows

def headerApplyList(id,usertype):
    conn = None
    cursor = None
    rows = None
    try:
        conn = dbInfo.dbConn()
        cursor = conn.cursor()
        if usertype == "1":
            sql = """
                    SELECT
                        b.regnum ,
                        (select username from tbl_users where id = b.rentalid ),
                        c.containernumber
                    FROM
                    tbl_container c
                    LEFT JOIN
                    tbl_booking b ON c.regnum = b.regnum
                    WHERE
                    c.id = %s
                    and b.bookingstatus ='N'
                """
        else:
            sql = """
                    SELECT
                        b.regnum,
                        (select username from tbl_users where id = b.registerid ),
                        c.containernumber
                    FROM
                    tbl_container c
                    LEFT JOIN
                    tbl_booking b ON c.regnum = b.regnum
                    WHERE
                    b.rentalid = %s
                    and b.bookingstatus ='Y'
                """
        cursor.execute(sql, (id,))  # <-- 튜플로 전달
        rows = cursor.fetchall()
    except Exception as e:
        print(f"헤더 신청 리스트 조회 실패 = {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows

def headerMessengerList(id):
    conn = None
    cursor = None
    rows = None
    try:
        conn = dbInfo.dbConn()
        cursor = conn.cursor()
        sql = """
                select 
                    messengernum,
                    (select 
                        containernumber 
                    from tbl_container 
                    where regnum = (
                                    select 
                                        regnum 
                                    from tbl_booking 
                                    where bookingnum = tm.bookingnum )
                                    ),
                    (select username from tbl_users where id = tm.id1),
                    (select username from tbl_users where id = tm.id2),
                    createtime 
                from tbl_messenger tm
                where id1 = %s
                or id2 = %s
                order by createtime asc
            """
        cursor.execute(sql, (id,id))  # <-- 튜플로 전달
        rows = cursor.fetchall()
    except Exception as e:
        print(f"헤더 메신저 리스트 조회 실패 = {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows

