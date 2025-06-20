from flask import Blueprint, request, jsonify, session
import google.generativeai as genai
from dotenv import load_dotenv
import os
# import psycopg2
from ..db import dbInfo
from ..predict.container_supply import predict_container_supply, extract_company_port
from ..predict.container_supply import predict_container_demand, extract_months_from_question

load_dotenv() 

chat_bp = Blueprint('chat', __name__, url_prefix="/chat")

# 환경변수에서 API 키 불러오기 (사전에 환경변수 설정 필요)
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

if not GENAI_API_KEY or not HUGGINGFACE_API_TOKEN:
    raise ValueError("API 키를 환경변수에 설정해주세요. GENAI_API_KEY, HUGGINGFACEHUB_API_TOKEN")

genai.configure(api_key=GENAI_API_KEY)
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACE_API_TOKEN

MODEL = None

def load_model():
    print("Loading Gemini model...")
    return genai.GenerativeModel('gemini-1.5-flash')

def initialize_chat_module():
    global MODEL
    if MODEL is None:
        MODEL = load_model()

# 앱 시작 시 모델 초기화
initialize_chat_module()

def sql_chatbot(question):
    myId = session.get('loginId')

    predict_keywords = ["예측", "예상", "미래", "forecast", "predict"]
    supply_keywords = ["공급", "등록량", "컨테이너 등록"]
    demand_keywords = ["수급", "예약량","수요", "요청", "book", "demand"]

    # 1) 예측 키워드 포함 시 예측 처리 우선 수행
    if any(word in question for word in predict_keywords + supply_keywords + demand_keywords):
        try:
            months = extract_months_from_question(question)
            company, port = extract_company_port(question)

            if any(word in question for word in demand_keywords):
                # 수급 예측
                result = predict_container_demand(period=f"{months}M", company=company, port=port)
                target = "수급"
                unit = "건"
                description = "예약이 이루어질 것으로 예상됩니다"
            else:
                # 공급 예측
                result = predict_container_supply(period=f"{months}M", company=company, port=port)
                target = "공급"
                unit = "개"
                description = "등록될 것으로 예상됩니다"

            if isinstance(result, dict) and result.get("error"):
                return "데이터가 부족하거나 조건에 맞는 정보가 없습니다.", "", ""

            total = sum(r['predicted_count'] for r in result)
            start = result[0]['period']
            end = result[-1]['period']
            is_forecast = all(r['source'] == 'forecast' for r in result)
            is_actual = all(r['source'] == 'actual' for r in result)

            monthly_lines = [
                f"- {r['period']}: 약 {r['predicted_count']}{unit} ({'예측' if r['source']=='forecast' else '실제'})"
                for r in result
            ]
            monthly_text = "\n".join(monthly_lines)

            if is_forecast:
                footer = "이 수치는 실제 데이터를 기반으로 예측된 값이며, 실제 상황과는 차이가 있을 수 있습니다."
            elif is_actual:
                footer = "이는 실제 기록된 데이터를 기반으로 한 결과입니다."
            else:
                footer = "실제 기록과 예측값이 혼합된 결과입니다."

            base_message = f"""
            [사용자 질문]
            {question}

            [{target} 예측 결과]
            총 {target} {unit}: {total}{unit}
            기간: {start} ~ {end}
            월별:
            {monthly_text}

            - 당신의 이름은 AnaBot입니다.
            - 위 결과는 컨테이너 {target} 데이터 기반으로 {description}.
            - 숫자 단위는 '{unit}'이며, 사용자에게 친근한 문장으로 안내하세요.
            - <br> 태그를 사용해 적절히 줄바꿈을 적용하세요.
            - 너무 기술적인 표현보다는 자연스럽고 이해하기 쉬운 말투로 작성하세요.
            {footer}
            """

            response = MODEL.generate_content(base_message)
            return response.text.strip(), "", response.text.strip()

        except Exception as e:
            error_msg = f"[에러] 예측 처리 중 문제가 발생했습니다:\n{e}"
            return error_msg, "", ""

    # 2) 예측 키워드가 없으면 테이블 관련성 판단
    schema = """
        [테이블: tbl_container]
        - regnum: 컨테이너 등록 고유 번호, 기본키
        - id: 컨테이너 등록자 ID
        - containernumber: 컨테이너 번호
        - size: 컨테이너 크기 (예: 20ft, 40ft)
        - tareweight: 공차중량(컨테이너 자체 무게)
        - terminal: 터미널 코드
        - location: 터미널 지역
        - porttype: 항구 종류(외항,내항)
        - availablefrom: 사용 가능 시작 날짜
        - availableto: 사용 가능 종료 날짜
        - rentaldays: 대여 가능 일수
        - priceperday: 하루 대여 비용
        - totalprice: 총 대여 비용
        - remarks: 비고
        - regdate: 등록 날짜

        [테이블: tbl_booking]
        - bookingnum: 예약 고유 번호
        - regnum: 컨테이너 등록 고유 번호 (tbl_container.regnum 참조)
        - rentalid: 컨테이너 등록자 ID
        - registerid: 예약자 ID
        - bookingstatus: 예약 상태 (Y:예약확정상태, N:예약진행상태)
        - bookingdate: 예약 생성 시각
    """

    check_prompt = f"""
        [테이블 스키마]
        {schema}

        [사용자 질문]
        {question}

        위 질문이 위 테이블 스키마와 관련이 있으면 "Y", 관련이 없으면 "N" 만 출력하세요.
    """
    check_response = MODEL.generate_content(check_prompt)
    is_related = check_response.text.strip().upper()

    if is_related != 'Y':
        answer_prompt = f"""
            아래는 일반 사용자의 질문입니다. 테이블과 관련이 없는 일상적이거나 자유로운 질문일 수 있습니다.

            [질문]
            {question}

            - 당신의 이름은 AnaBot입니다.
            - 질문에 대해 당신의 생각을 바탕으로 자연스럽고 따뜻하게 답변하세요.
            - 너무 기술적이거나 딱딱하지 않게, 부드럽고 명료하게 말해주세요.
            - 데이터베이스나 SQL 관련 설명은 포함하지 마세요.
            - 필요한 경우 <br>을 적절히 사용하여 줄바꿈 표현하세요.
        """
        response = MODEL.generate_content(answer_prompt)
        return response.text.strip(), "", response.text.strip()

    # 3) 관련 질문일 경우 SQL 생성 및 실행
    prompt = f"""
        당신은 SQL 전문가입니다. 아래는 PostgreSQL 데이터베이스의 테이블 스키마입니다.

        [테이블 스키마]
        {schema}

        [내 아이디]
        {myId}

        [사용자 질문]
        {question}

        [규칙]
        - 무조건 PostgreSQL 문법으로 작성하세요.
        - tbl_container의 데이터는 등록 된 컨테이너 입니다.
        - 예약 가능한 컨테이너는 tbl_booking에 존재하지 않는 regnum을 가진 tbl_container의 데이터입니다.
        - tbl_booking의 regnum은 tbl_container의 regnum을 참조하며 bookingstatus (Y:예약확정상태, N:예약진행상태) 입니다.
        - 예약확정상태, 예약진행상태면 예약신청을 할 수 없습니다.
        - (availablefrom: 사용 가능 시작 날짜)가 오늘 날짜 이후일 경우만 예약신청을 할 수 있습니다.
        - 질문에 대한 적절한 SQL 쿼리를 PostgreSQL 문법으로 작성하세요.
        - SQL 외 다른 설명은 하지 마세요.
        - 컨테이너 정보의 조회는 availablefrom 오름차순으로 하세요.
        - 쿼리 결과는 LIMIT 5으로 제한하세요.
        SQL:
    """

    sql = ""
    try:
        response = MODEL.generate_content(prompt)
        sql = response.text.strip().strip("```sql").strip("```")
        print("[생성된 SQL 쿼리]:", sql)

        columns, rows = execute_sql_and_return_results(sql)

        result_text = "\n".join([", ".join(map(str, row)) for row in rows])
        column_text = ", ".join(columns)

        prompt_answer = f"""
            사용자 질문: {question}
            실행한 SQL: {sql}
            결과 행의 수 : {len(rows)}
            결과 컬럼: {column_text}
            결과 데이터: {result_text}
            테이블 스키마: {schema}

            - 당신의 이름은 AnaBot입니다.
            - 위 정보를 바탕으로 사용자에게 친절하고 자연스럽게 한국어로 답변 하세요.
            - 너무 기술적인 설명은 피하고, 간단 명료하게 말해 주세요.
            - 줄바꿈이 생길때 텍스트 사이에 <br>을 추가하세요
            - 질문이 스키마의 내용과 관련이 없다 판단되면 그에 맞는 대답을 하세요.
            - 무조건 컨테이너 정보를 알려 줄 시에만 
                <a href="javascript:void(0);" onclick="postToDetail('regNum')">;containernumber,terminal,availablefrom,availableto,totalprice</a>의 정보로 알려주세요.
            - 사용자가 "컨테이너 수", "예약 가능 컨테이너 수"처럼 **숫자나 요약** 정보를 물으면, **상세 컨테이너 정보는 제공하지 마세요.**
            - '총 대여료', '대여 기간', '개수' 등의 항목은 사용자 친화적인 용어(예: 금액, 일 수, 수량 등)로 자연스럽게 표현하세요.     
            - 결과 행의 수가 5일 경우만 [검색 결과는 최대 5개 까지 가능합니다.] 라고 가장 마지막에 <br><br> 추가 후 답변 하세요.
        """
        response_answer = MODEL.generate_content(prompt_answer)
        answer = response_answer.text.strip()

        return answer, sql, answer

    except Exception as e:
        return f"[에러] SQL 실행 중 문제가 발생했습니다:\n{e} <br><br>같은 질문 후 같은 현상 시 관리자에게 문의하세요.", sql, ""


@chat_bp.route("/sql-query", methods=["POST"])
def chatbot_sql():
    json_data = request.get_json()
    question = json_data.get("message")

    add_to_chat_history("user", question)

    result, sql, answer = sql_chatbot(question)

    add_to_chat_history("bot", result)

    return jsonify({"result": result, "sql": sql, "answer": answer})

@chat_bp.route("/history", methods=["GET"])
def chat_history():
    return jsonify(session.get("chat_history", []))

def add_to_chat_history(role, message):
    if "chat_history" not in session:
        session["chat_history"] = []
    session["chat_history"].append({"role": role, "message": message})
    session.modified = True

def execute_sql_and_return_results(sql):
    conn = None
    try:
        conn = dbInfo.dbConn()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return columns, rows
    except Exception as e:
        raise RuntimeError(f"SQL 실행 오류: {e}")
    finally:
        if conn:
            conn.close()