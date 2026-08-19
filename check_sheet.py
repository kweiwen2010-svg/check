import streamlit as st
import gspread
import textwrap
from google.oauth2.service_account import Credentials

st.title("Google Sheets 連線測試")

def get_gspread_client():
    try:
        creds_dict = dict(st.secrets["gcp_service_account"])
        
        # 取得純亂碼金鑰
        raw_key = creds_dict["private_key"].strip()
        
        # 自動每 64 個字元切一行（這是 PEM 格式標準規範）
        wrapped_key = "\n".join(textwrap.wrap(raw_key, 64))
        
        # 自動組裝完整的 PEM 格式框架
        creds_dict["private_key"] = f"-----BEGIN PRIVATE KEY-----\n{wrapped_key}\n-----END PRIVATE KEY-----"
        
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