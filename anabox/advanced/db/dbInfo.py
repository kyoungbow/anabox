import psycopg2
## 중복 아이디 체크

def dbConn():
    conn = psycopg2.connect(
        dbname="containerSharing_test",
        user="kyoungbow",
        password="1234",
        host="localhost",
        port="5432"
    )
    # 클라이언트 인코딩 설정
    conn.set_client_encoding('UTF8')
    return conn