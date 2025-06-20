import psycopg2
from . import dbInfo

## 컨테이너 리스트 조회
def selectCompany(id):
    conn = None
    cursor = None
    rows = None
    try:
        conn = dbInfo.dbConn()
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
        cursor.execute(sql, (id,))  # <-- 튜플로 전달
        rows = cursor.fetchone()
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

