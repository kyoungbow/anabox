from flask import Blueprint,render_template,request,jsonify,session
import json
from ..db import stats_util
from datetime import datetime
import pandas as pd

stats_bp = Blueprint("stats", __name__, url_prefix="/stats")

# # 선사별
# @stats_bp.route("/stats", methods=['GET', 'POST'])
# def stats():
#     if request.method == 'POST':
#         id = request.form.get('userId', session.get('loginId'))
#     else:
#         id = request.args.get('userId', session.get('loginId'))
#     row = company_util.selectCompany(id)
#     return render_template("company/company.html", row=row)


# 선사별
@stats_bp.route("/sadStats", methods=['GET', 'POST'])
def sadStats():
    return render_template("stats/sadStats.html")


@stats_bp.route("/selectYears", methods=['GET', 'POST'])
def selectYears():
    rows = stats_util.selectYears()
    return jsonify(rows)

@stats_bp.route("/selectCompany", methods=['GET', 'POST'])
def selectCompany():
    rows = stats_util.selectCompany()
    return jsonify(rows)

@stats_bp.route("/selectLocation", methods=['GET', 'POST'])
def selectLocation():
    rows = stats_util.selectLocation()
    return jsonify(rows)

from flask import request, jsonify
import traceback

@stats_bp.route("/selectChartData", methods=['POST'])
def selectChartData():
    company = request.form.get('company', "")
    location = request.form.get('location', "")
    year = request.form.get('year', "")
    try:
        rows = stats_util.selectChartData(company, location, year)

        result = [
            {
                "id": r[0],
                "year_month": r[1].strftime('%Y-%m-%d'),
                "supply_count": r[2],
                "requested_bookings": r[3],
                "confirmed_bookings": r[4],
                "pending_bookings": r[5],
                "unbooked_supply": r[6]
            }
            for r in rows
        ]

        return jsonify({"success": True, "data": result})

    except Exception as e:
        print(f"차트 데이터 조회 실패: {e}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": "차트 데이터 조회 중 오류가 발생했습니다. 관리자에게 문의하세요."
        }), 500

