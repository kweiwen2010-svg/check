import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.title("Google Sheets 連線測試")

def get_gspread_client():
    try:
        creds_dict = dict(st.secrets["gcp_service_account"])
        
        # 強制把私鑰裡面所有寫出來的 \n 或多餘空白全部轉成真實的換行字元
        raw_key = creds_dict["private_key"]
        # 確保開頭與結尾正確，並將跳脫字元轉回換行
        clean_key = raw_key.replace("\\n", "\n")
        creds_dict["private_key"] = clean_key
        
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