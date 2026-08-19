import streamlit as st
import gspread
import json
from google.oauth2.service_account import Credentials

st.title("Google Sheets 連線測試")

def get_gspread_client():
    try:
        # 這裡要對應剛才改好的 key 名稱
        raw_json = st.secrets["json_str"]
        creds_dict = json.loads(raw_json)
        
        if "private_key" in creds_dict:
            creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
        
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"憑證解析錯誤: {e}")
        return None

if st.button("開始測試連線"):
    client = get_gspread_client()
    if client:
        st.success("✅ 連線成功！")