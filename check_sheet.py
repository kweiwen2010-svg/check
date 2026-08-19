import streamlit as st
import gspread
import json
from google.oauth2.service_account import Credentials

st.title("Google Sheets 連線測試")

def get_gspread_client():
    try:
        # 直接讀取完整的 JSON 字串並轉為字典
        json_str = st.secrets["gcp_service_account"]["json_key"]
        creds_dict = json.loads(json_str)
        
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
        st.success("✅ 手機端憑證解析成功！")