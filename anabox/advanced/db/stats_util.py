import psycopg2
from . import dbInfo

## 컨테이너 리스트 조회
def selectYears():
    conn = None
    cursor = None
    rows = None
    try:
        conn = dbInfo.dbConn()
        cursor = conn.cursor()
        sql = """
                select 
                    distinct(EXTRACT(YEAR FROM availablefrom)) 
                from tbl_container 
                order by 1 asc
                """
        cursor.execute(sql)  # <-- 튜플로 전달
        rows = cursor.fetchall()
    except Exception as e:
        print(f"연도 조회 오류 = {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows

def selectCompany():
    conn = None
    cursor = None
    rows = None
    try:
        conn = dbInfo.dbConn()
        cursor = conn.cursor()
        sql = """
                select 
                    distinct(company) 
                from tbl_users 
                where usertype = 1
                order by 1 asc
                """
        cursor.execute(sql)  # <-- 튜플로 전달
        rows = cursor.fetchall()
    except Exception as e:
        print(f"회사 조회 오류 = {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows


def selectLocation():
    conn = None
    cursor = None
    rows = None
    try:
        conn = dbInfo.dbConn()
        cursor = conn.cursor()
        sql = """
                select 
                    distinct(location)
                from tbl_container
                order by 1 asc
                """
        cursor.execute(sql)  # <-- 튜플로 전달
        rows = cursor.fetchall()
    except Exception as e:
        print(f"항만 조회 오류 = {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows

def selectChartData(company, location, year):
    conn = None
    cursor = None
    rows = None
    try:
        conn = dbInfo.dbConn()
        cursor = conn.cursor()
        sql = """
            SELECT
                c.id,
                DATE_TRUNC('month', c.availablefrom)::date AS year_month,
                COUNT(*) AS supply_count,
                COUNT(CASE WHEN b.bookingstatus IN ('Y', 'N') THEN 1 END) AS requested_bookings,
                COUNT(CASE WHEN b.bookingstatus = 'Y' THEN 1 END) AS confirmed_bookings,
                COUNT(CASE WHEN b.bookingstatus = 'N' THEN 1 END) AS pending_bookings,
                COUNT(CASE WHEN b.regnum IS NULL THEN 1 END) AS unbooked_supply
            FROM
                public.tbl_container c
            LEFT JOIN
                public.tbl_booking b 
                ON b.regnum = c.regnum
            WHERE
                EXTRACT(YEAR FROM c.availablefrom) = %s
        """
        params = [year]  # 파라미터 리스트 생성

        if company != "":
            sql += """
                AND c.id IN (SELECT id FROM tbl_users WHERE company = %s)
            """
            params.append(company)

        if location != "":
            sql += """
                AND c.location = %s
            """
            params.append(location)

        sql += """
            GROUP BY
                c.id, year_month
            ORDER BY
                c.id, year_month
        """
        cursor.execute(sql, tuple(params))  # 파라미터 튜플로 전달
        rows = cursor.fetchall()

    except Exception as e:
        print(f"차트 데이터 조회 오류 = {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return rows


