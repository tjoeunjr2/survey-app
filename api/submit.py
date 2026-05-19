import gspread
from google.oauth2.service_account import Credentials
import os
import json
from datetime import datetime

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_sheet():
    creds_dict = json.loads(os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON"))
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(os.environ.get("SPREADSHEET_ID")).sheet1
    return sheet

def handler(request, response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"

    if request.method == "OPTIONS":
        return response.send("ok", 200)

    try:
        data = request.json
        sheet = get_sheet()

        if not sheet.get_all_values() or sheet.cell(1,1).value != "타임스탬프":
            sheet.insert_row(["타임스탬프","이름","연령대","만족도","이용빈도","추천여부","의견"], index=1)

        sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data.get("name", "익명"),
            data.get("age_group", ""),
            data.get("satisfaction", ""),
            data.get("frequency", ""),
            data.get("recommend", ""),
            data.get("comment", "")
        ])

        return response.json({"success": True})
    except Exception as e:
        return response.json({"success": False, "error": str(e)}, 500)
