import pandas as pd
from prophet import Prophet
from datetime import datetime
import psycopg2
from ..db import dbInfo
import re


def get_container_data(company=None, port=None):
    """
    회사명과 항만명을 기준으로 월별 컨테이너 등록량을 집계하여 반환
    """
    params = []
    where_clauses = ["c.availablefrom IS NOT NULL"]

    if company:
        where_clauses.append("c.id = (SELECT id FROM tbl_users WHERE company = %s)")
        params.append(company)
    if port:
        where_clauses.append("c.location = %s")
        params.append(port)

    where_sql = " AND ".join(where_clauses)

    sql = f"""
        SELECT
            DATE_TRUNC('month', c.availablefrom) AS month,
            COUNT(*) AS container_count
        FROM tbl_container c
        WHERE {where_sql}
        GROUP BY month
        ORDER BY month
    """

    conn = dbInfo.dbConn()
    df = pd.read_sql(sql, conn, params=params)
    conn.close()

    if not df.empty and pd.api.types.is_datetime64tz_dtype(df['month']):
        df['month'] = df['month'].dt.tz_localize(None)

    return df

# 공급예측
def predict_container_supply(period='1M', company=None, port=None):
    df = get_container_data(company=company, port=port)
    if df.empty:
        return {"error": f"{company or ''} {port or ''} 조건에 해당하는 데이터가 없습니다."}

    # 오늘 기준 다음 n개월 예측
    months = int(period[:-1]) if period.endswith('M') else 1
    today = pd.Timestamp.today().replace(day=1)
    target_months = [today + pd.DateOffset(months=i) for i in range(1, months + 1)]

    # 실제 값이 있는 경우 먼저 반환
    results = []
    for month in target_months:
        if month in df['month'].values:
            actual_count = int(df[df['month'] == month]['container_count'].values[0])
            results.append({
                "period": month.strftime('%Y-%m'),
                "predicted_count": actual_count,
                "source": "actual"
            })

    # 예측이 필요한 경우 Prophet 수행
    needed_months = [m for m in target_months if m not in df['month'].values]
    if needed_months:
        df_prophet = df.rename(columns={'month': 'ds', 'container_count': 'y'})
        model = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
        model.fit(df_prophet)

        future = pd.DataFrame({'ds': needed_months})
        forecast = model.predict(future)

        for _, row in forecast.iterrows():
            results.append({
                "period": row['ds'].strftime('%Y-%m'),
                "predicted_count": int(round(row['yhat'])),
                "source": "forecast"
            })

    # 정렬
    results.sort(key=lambda x: x['period'])
    return results


def get_booking_data(company=None, port=None):
    params = []
    where_clauses = ["b.bookingstatus = 'Y'", "c.availablefrom IS NOT NULL"]

    if company:
        where_clauses.append("c.id = (SELECT id FROM tbl_users WHERE company = %s)")
        params.append(company)
    if port:
        where_clauses.append("c.location = %s")
        params.append(port)

    where_sql = " AND ".join(where_clauses)

    sql = f"""
        SELECT
            DATE_TRUNC('month', c.availablefrom) AS month,
            COUNT(*) AS booking_count
        FROM tbl_booking b
        JOIN tbl_container c ON b.regnum = c.regnum
        WHERE {where_sql}
        GROUP BY month
        ORDER BY month
    """

    conn = dbInfo.dbConn()
    df = pd.read_sql(sql, conn, params=params)
    conn.close()

    if not df.empty and pd.api.types.is_datetime64tz_dtype(df['month']):
        df['month'] = df['month'].dt.tz_localize(None)

    return df


# 수급 예측
def predict_container_demand(period='1M', company=None, port=None):
    df = get_booking_data(company=company, port=port)
    print(f"df={df}")
    if df.empty:
        return {"error": f"{company or ''} {port or ''} 조건에 해당하는 수요 데이터가 없습니다."}

    if df.shape[0] < 2:
        return {"error": f"{company or ''} {port or ''} 조건의 예약 건수가 2건 미만이라 예측이 어렵습니다."}

    # 오늘 기준 다음 n개월 예측
    months = int(period[:-1]) if period.endswith('M') else 1
    today = pd.Timestamp.today().replace(day=1)
    target_months = [today + pd.DateOffset(months=i) for i in range(1, months + 1)]

    # 실제 값이 있는 경우
    results = []
    for month in target_months:
        if month in df['month'].values:
            actual_count = int(df[df['month'] == month]['booking_count'].values[0])
            results.append({
                "period": month.strftime('%Y-%m'),
                "predicted_count": actual_count,
                "source": "actual"
            })

    # 예측이 필요한 경우 Prophet 수행
    needed_months = [m for m in target_months if m not in df['month'].values]
    if needed_months:
        df_prophet = df.rename(columns={'month': 'ds', 'booking_count': 'y'})
        model = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
        model.fit(df_prophet)

        future = pd.DataFrame({'ds': needed_months})
        forecast = model.predict(future)

        for _, row in forecast.iterrows():
            results.append({
                "period": row['ds'].strftime('%Y-%m'),
                "predicted_count": int(round(row['yhat'])),
                "source": "forecast"
            })

    # 정렬
    results.sort(key=lambda x: x['period'])
    return results

# 공급 예측
def extract_company_port(question: str):
    """
    사용자 질문에서 회사명(company)과 지역명(location)을 추출
    - '부산항', '울산항' 등 항구 관련 단어도 '부산', '울산' 등으로 매핑되도록 처리
    """
    conn = dbInfo.dbConn()

    company_sql = "SELECT DISTINCT company FROM tbl_users"
    port_sql = "SELECT DISTINCT location FROM tbl_container"

    company_df = pd.read_sql(company_sql, conn)
    port_df = pd.read_sql(port_sql, conn)
    conn.close()

    company_list = company_df['company'].dropna().tolist()
    port_list = port_df['location'].dropna().tolist()

    # 질문 전처리: (주), 항, 공백 제거
    question_clean = question.replace("(주)", "").replace("항", "").replace(" ", "").lower()

    # 회사명 매칭 (전처리 후 비교)
    matched_company = None
    for c in company_list:
        c_clean = c.replace("(주)", "").replace(" ", "").lower()
        if c_clean in question_clean:
            matched_company = c
            break

    # 포트명 매칭
    matched_port = None
    for p in port_list:
        p_clean = p.replace(" ", "").lower()
        if p_clean in question_clean:
            matched_port = p
            break

    return matched_company, matched_port


def extract_months_from_question(question: str) -> int:
    question = question.lower()

    # 한글 숫자 매핑
    kor_num_map = {
        '한': 1,
        '두': 2,
        '세': 3,
        '네': 4,
        '다섯': 5,
        '여섯': 6,
        '일곱': 7,
        '여덟': 8,
        '아홉': 9,
        '열': 10
    }

    # 숫자+개월
    match_month = re.search(r'(\d+)\s*개월', question)
    if match_month:
        return int(match_month.group(1))

    # 숫자+년
    match_year = re.search(r'(\d+)\s*년', question)
    if match_year:
        return int(match_year.group(1)) * 12

    # 숫자+주
    match_week = re.search(r'(\d+)\s*주', question)
    if match_week:
        weeks = int(match_week.group(1))
        months_from_weeks = max(1, round(weeks / 4))
        return months_from_weeks

    # 한글 숫자 + 달
    for kor_num, val in kor_num_map.items():
        if kor_num + '달' in question:
            return val

    # 자연어 기간 표현들
    if '다음달' in question or '다음 달' in question or '이번달' in question or '이번 달' in question:
        return 1
    if '다다음달' in question or '다다음 달' in question:
        return 2
    if '내년' in question or '1년 후' in question:
        return 12
    if '분기' in question:
        return 3
    if '반기' in question:
        return 6
    if '다음주' in question or '다음 주' in question:
        return 1
    if '내일' in question or '오늘' in question:
        return 1

    return 3


