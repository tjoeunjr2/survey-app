import gspread
from google.oauth2.service_account import Credentials
import os
import json
from collections import Counter

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

    if request.method == "OPTIONS":
        return response.send("ok", 200)

    try:
        sheet = get_sheet()
        all_rows = sheet.get_all_records()

        return response.json({
            "total": len(all_rows),
            "age_group": dict(Counter(r["연령대"] for r in all_rows)),
            "satisfaction": dict(Counter(r["만족도"] for r in all_rows)),
            "frequency": dict(Counter(r["이용빈도"] for r in all_rows)),
            "recommend": dict(Counter(r["추천여부"] for r in all_rows))
        })
    except Exception as e:
        return response.json({"error": str(e)}, 500)
