import streamlit as st
import gspread
import json
from google.oauth2.service_account import Credentials

def get_gspread_client():
    try:
        # 將 secrets 轉為字典
        creds_dict = dict(st.secrets["gcp_service_account"])
        
        # 強制修復：使用 encode().decode('unicode_escape') 處理 \n
        # 這會把文字中的 "\n" 轉換為真正的系統換行符號
        creds_dict["private_key"] = creds_dict["private_key"].encode("utf-8").decode("unicode_escape")
        
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"憑證解析錯誤: {e}")
        return None

# 執行
client = get_gspread_client()
if client:
    st.success("✅ 手機端憑證解析成功！")