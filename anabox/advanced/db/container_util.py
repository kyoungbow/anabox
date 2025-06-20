import psycopg2
from . import dbInfo

## 컨테이너 리스트 조회
def selectContainerList(userId,availableFrom,availableTo,userType,route):
    conn = None
    cursor = None
    rows = None
    try:
        conn = dbInfo.dbConn()
        cursor = conn.cursor()
        print()
        if route == "index":
            sql = """
                        SELECT 
                            a.* 
                        FROM 
                            tbl_container a
                        LEFT JOIN 
                            tbl_booking b ON a.regnum = b.regnum
                        WHERE 
                            a.availableFrom >= %s
                            AND a.availableTo <= %s
                            AND b.regnum IS NULL
                        """
            cursor.execute(sql, (availableFrom,availableTo))  # <-- 튜플로 전달
        else : 
            if userType == "1":
                sql = """
                        SELECT 
                            a.* 
                        FROM 
                            tbl_container a
                        LEFT JOIN 
                            tbl_booking b ON a.regnum = b.regnum
                        WHERE 
                            a.id = %s
                            AND a.availableFrom >= %s
                            AND a.availableTo <= %s
                            AND b.regnum IS NULL
                        """
                cursor.execute(sql, (userId,availableFrom,availableTo))  # <-- 튜플로 전달
            else :
                sql = """
                        SELECT 
                            a.* 
                        FROM 
                            tbl_container a
                        LEFT JOIN 
                            tbl_booking b ON a.regnum = b.regnum
                        WHERE 
                            a.availableFrom >= %s
                            AND a.availableTo <= %s
                            AND b.regnum IS NULL
                        """
                cursor.execute(sql, (availableFrom,availableTo))  # <-- 튜플로 전달
        rows = cursor.fetchall()
    except Exception as e:
        print(f"컨테이너 리스트 조회 오류 = {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows

## 부킹 리스트 조회
def selectBookingList(userId, availableFrom, availableTo, bookingStatus,usertype):
    conn = None
    cursor = None
    rows = None
    try:
        conn = dbInfo.dbConn()
        cursor = conn.cursor()
        if usertype == "1" :
            sql = """
                    SELECT 
                        a.* 
                    FROM 
                        tbl_container a
                    LEFT JOIN 
                        tbl_booking b ON a.regnum = b.regnum
                    WHERE 
                        b.registerid = %s
                        AND a.availableFrom >= %s
                        AND a.availableTo <= %s
                        AND b.regnum IS NOT NULL AND b.bookingStatus = %s
                    """
        else :
            sql = """
                    SELECT 
                        a.* 
                    FROM 
                        tbl_container a
                    LEFT JOIN 
                        tbl_booking b ON a.regnum = b.regnum
                    WHERE 
                        b.rentalid = %s
                        AND a.availableFrom >= %s
                        AND a.availableTo <= %s
                        AND b.regnum IS NOT NULL AND b.bookingStatus = %s
                    """
        cursor.execute(sql, (userId,availableFrom,availableTo,bookingStatus))  # <-- 튜플로 전달
        rows = cursor.fetchall()
    except Exception as e:
        print(f"컨테이너 예약 리스트 조회 오류 = {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows

## 디테일 조회
def selectContainerDetail(param):
    conn = None
    cursor = None
    rows = None
    try:
        conn = dbInfo.dbConn()
        cursor = conn.cursor()
        sql = "select * from tbl_container where regnum = %s"
        cursor.execute(sql, (param,))  # <-- 튜플로 전달
        rows = cursor.fetchone()
    except Exception as e:
        print(f"컨테이터 조회 실패 = {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows

## 컨테이너 등록
def register(id,containerNumber,size,tareWeight,terminal,location,portType,availableFrom,availableTo,rentalDays,pricePerDay,totalPrice,remarks):
    conn = None
    cursor = None
    try:
        conn =  dbInfo.dbConn()
        cursor = conn.cursor()

        sql = """insert into tbl_container 
                    (id,containerNumber,size,tareWeight,terminal,location,portType,availableFrom,availableTo,rentalDays,pricePerDay,totalPrice,remarks) 
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql,(id,containerNumber,size,tareWeight,terminal,location,portType,availableFrom,availableTo,rentalDays,pricePerDay,totalPrice,remarks))
        conn.commit()
    except Exception as e :
        print(f"컨테이너 등록 오류 == {e}")
        if conn: # DML 구문에서는 넣어줘야 함
            conn.rollback()
        raise
    finally:
        if cursor :
            cursor.close()
        if conn :
            conn.close()

## 삭제
def delete(regNum,userId):
    conn = None
    cursor = None
    try:
        conn =  dbInfo.dbConn()
        cursor = conn.cursor()

        sql = """
                delete from tbl_container
                where regNum = %s
                and id = %s
                """
        cursor.execute(sql,(regNum,userId))
        conn.commit()
    except Exception as e :
        print(f"컨테이너 삭제 오류 == {e}")
        if conn: # DML 구문에서는 넣어줘야 함
            conn.rollback()
        raise
    finally:
        if cursor :
            cursor.close()
        if conn :
            conn.close()

def update(regNum, id, containerNumber,
           size, tareWeight, terminal, location,
           portType,availableFrom,availableTo,
           rentalDays,pricePerDay,totalPrice,
           remarks):
    conn = None
    cursor = None
    try:
        conn =  dbInfo.dbConn()
        cursor = conn.cursor()

        sql = """
                    UPDATE tbl_container
                    SET
                        containerNumber = %s,
                        size = %s,
                        tareWeight = %s,
                        terminal = %s,
                        location = %s,
                        portType = %s,
                        availableFrom = %s,
                        availableTo = %s,
                        rentalDays = %s,
                        pricePerDay = %s,
                        totalPrice = %s,
                        remarks = %s
                    WHERE
                        regnum = %s and
                        id = %s
                """
        cursor.execute(sql,(containerNumber,
                            size,
                            tareWeight,
                            terminal,
                            location,
                            portType,
                            availableFrom,
                            availableTo,
                            rentalDays,
                            pricePerDay,
                            totalPrice,
                            remarks,
                            regNum,
                            id))
        conn.commit()
    except Exception as e :
        print(f"컨테이너 수정 오류 == {e}")
        if conn: # DML 구문에서는 넣어줘야 함
            conn.rollback()
        raise
    finally:
        if cursor :
            cursor.close()
        if conn :
            conn.close()

## 디테일 조회
def selectBookingDetail(param):
    conn = None
    cursor = None
    rows = None
    try:
        conn = dbInfo.dbConn()
        cursor = conn.cursor()
        sql = """
                SELECT 
                    a.*,
                    b.*
                FROM 
                    tbl_container a
                LEFT JOIN 
                    tbl_booking b ON a.regnum = b.regnum
                WHERE 
                    a.regnum = %s
                    AND b.regnum is Not NULL
                """
        cursor.execute(sql, (param,))  # <-- 튜플로 전달
        rows = cursor.fetchone()
    except Exception as e:
        print(f"예약 상세 조회 실패 = {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows

## 예약 취소
def bookingCancel(bookingNum,regNum):
    conn = None
    cursor = None
    try:
        conn =  dbInfo.dbConn()
        cursor = conn.cursor()

        sql = """
                delete from tbl_booking
                where bookingNum = %s
                and regNum = %s
                """
        cursor.execute(sql,(bookingNum,regNum))
        conn.commit()
    except Exception as e :
        print(f"예약 삭제 오류 == {e}")
        if conn: # DML 구문에서는 넣어줘야 함
            conn.rollback()
        raise
    finally:
        if cursor :
            cursor.close()
        if conn :
            conn.close()

# 예약 확정
def booking(bookingNum,regNum):
    conn = None
    cursor = None
    try:
        conn =  dbInfo.dbConn()
        cursor = conn.cursor()
        sql = """
                    UPDATE tbl_booking
                    SET
                        bookingStatus = 'Y'
                    WHERE bookingNum = %s
                    and regNum = %s
                """
        cursor.execute(sql,(bookingNum,regNum))
        conn.commit()
    except Exception as e :
        print(sql)
        print(f"예약 확정 오류 == {e}")
        if conn: # DML 구문에서는 넣어줘야 함
            conn.rollback()
        raise
    finally:
        if cursor :
            cursor.close()
        if conn :
            conn.close()

# 예약 확정 취소
def bookingConfirmCancel(bookingNum,regNum):
    conn = None
    cursor = None
    try:
        conn =  dbInfo.dbConn()
        cursor = conn.cursor()
        sql = """
                    UPDATE tbl_booking
                    SET
                        bookingStatus = 'N'
                    WHERE bookingNum = %s
                    and regNum = %s
                """
        cursor.execute(sql,(bookingNum,regNum))
        conn.commit()
    except Exception as e :
        print(sql)
        print(f"예약 확정 취소 오류 == {e}")
        if conn: # DML 구문에서는 넣어줘야 함
            conn.rollback()
        raise
    finally:
        if cursor :
            cursor.close()
        if conn :
            conn.close()

def bookingApply(regNum,userId,registerId):
    conn = None
    cursor = None
    try:
        conn =  dbInfo.dbConn()
        cursor = conn.cursor()

        sql = """insert into tbl_booking (regnum, rentalid, registerid, bookingstatus)
                values (%s,%s,%s,'N')"""
        cursor.execute(sql,(regNum,userId,registerId))
        conn.commit()
    except Exception as e :
        print(f"예약 신청 오류 == {e}")
        if conn: # DML 구문에서는 넣어줘야 함
            conn.rollback()
        raise
    finally:
        if cursor :
            cursor.close()
        if conn :
            conn.close()

# 예약 번호 조회
def selectBookingNum(regNum,userId,registerId):
    conn = None
    cursor = None
    rows = None
    try:
        conn = dbInfo.dbConn()
        cursor = conn.cursor()
        sql = """
                select 
                    bookingnum 
                from tbl_booking
                where regnum = %s
                and rentalid = %s
                and registerid = %s
                """
        cursor.execute(sql, (regNum,userId,registerId))  # <-- 튜플로 전달
        rows = cursor.fetchone()
    except Exception as e:
        print(f"예약 번호 조회 = {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows


# 채팅방 생성
def createMessenger(bookingNum,userId,registerId):
    conn = None
    cursor = None
    try:
        conn =  dbInfo.dbConn()
        cursor = conn.cursor()

        sql = """
                INSERT INTO tbl_messenger
                ( bookingnum, id1, id2)
                VALUES(%s, %s, %s);
                """
        cursor.execute(sql,(bookingNum,userId,registerId))
        conn.commit()
    except Exception as e :
        print(f"채팅방 생성 오류 == {e}")
        if conn: # DML 구문에서는 넣어줘야 함
            conn.rollback()
        raise
    finally:
        if cursor :
            cursor.close()
        if conn :
            conn.close()

# 채팅방 삭제
def deleteMessenger(bookingNum):
    conn = None
    cursor = None
    try:
        conn =  dbInfo.dbConn()
        cursor = conn.cursor()

        sql = """
                delete from tbl_messenger
                where bookingNum = %s
            """
        cursor.execute(sql,(bookingNum,))
        conn.commit()
    except Exception as e :
        print(f"채팅방 삭제 오류 == {e}")
        if conn: # DML 구문에서는 넣어줘야 함
            conn.rollback()
        raise
    finally:
        if cursor :
            cursor.close()
        if conn :
            conn.close()

## 컨테이너 대량 등록
def bulkRegister(userId, dataList):
    conn = None
    cursor = None
    try:
        conn = dbInfo.dbConn()
        cursor = conn.cursor()
        for data in dataList:
            containerNumber = data.get('containerNumber')
            size = data.get('size')
            tareWeight = data.get('tareWeight')
            terminal = data.get('terminal')
            location = data.get('location')
            portType = data.get('portType')
            availableFrom = data.get('availableFrom')
            availableTo = data.get('availableTo')
            rentalDays = data.get('rentalDays')
            pricePerDay = data.get('pricePerDay')
            totalPrice = data.get('totalPrice')
            remarks = data.get('remarks')

            sql = """INSERT INTO tbl_container 
                     (id, containerNumber, size, tareWeight, terminal, location, portType, availableFrom, availableTo, rentalDays, pricePerDay, totalPrice, remarks) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (userId, containerNumber, size, tareWeight, terminal, location, portType, availableFrom, availableTo, rentalDays, pricePerDay, totalPrice, remarks))
        conn.commit()
    except Exception as e:
        print(f"컨테이너 대량 등록 오류 == {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
