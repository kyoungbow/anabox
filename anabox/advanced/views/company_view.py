from flask import Blueprint,render_template,request,jsonify,session
import json
from ..db import company_util
from datetime import datetime
import pandas as pd

company_bp = Blueprint("company", __name__, url_prefix="/company")

# 회사 소개
@company_bp.route("/company", methods=['GET', 'POST'])
def company():
    if request.method == 'POST':
        id = request.form.get('userId', session.get('loginId'))
    else:
        id = request.args.get('userId', session.get('loginId'))
    row = company_util.selectCompany(id)
    return render_template("company/company.html", row=row)
    
