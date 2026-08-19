import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json

st.title("🔍 Google Sheets 連線自我檢查")

# 1. 輸入你的 Google Sheet 名稱或完整網址
sheet_name = st.text_input("輸入你的 Google Sheet 名稱", value="你的_Google_Sheet_名稱")

# 2. 檢查 Streamlit Secrets 是否正確設定
st.subheader("1. 檢查 Secrets 設定")
if "gcp_service_account" in st.secrets:
    st.success("✅ 偵測到 `st.secrets['gcp_service_account']`")
    
    # 嘗試解析憑證
    try:
        creds_dict = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ],
        )
        st.success("✅ Service Account 憑證格式正確！")
        st.info(f"服務帳號 Email: `{creds.service_account_email}`")
        
        # 提醒使用者去 Google Sheet 共用
        st.warning(f"⚠️ 請務必確認你的 Google Sheet 已經分享（共用）給這個 Email：\n`{creds.service_account_email}`")
        
    .except Exception as e:
        st.error(f"❌ 憑證解析失敗，格式可能寫錯：\n`{e}`")
        st.stop()
else:
    st.error("❌ 找不到 `gcp_service_account`！請檢查你的 `.streamlit/secrets.toml` 或 Streamlit Cloud 後台的 Secrets 設定。")
    st.stop()

# 3. 測試實際讀取 Google Sheet
st.subheader("2. 測試連線與讀取")
if st.button("開始測試讀取"):
    try:
        client = gspread.authorize(creds)
        
        # 嘗試開啟試算表
        sh = client.open(sheet_name)
        st.success(f"🎉 成功連線並開啟試算表：`{sheet_name}`")
        
        # 嘗試讀取第一個工作表的第一列資料
        worksheet = sh.get_worksheet(0)
        data = worksheet.get_all_records()
        st.write(f"✅ 成功讀取資料！目前工作表名稱：`{worksheet.title}`")
        st.json(data[:3]) # 顯示前三筆資料預覽
        
    except gspread.exceptions.SpreadsheetNotFound:
        st.error(f"❌ 找不到名為 `{sheet_name}` 的試算表。請確認名稱是否完全正確，且已分享給服務帳號。")
    except Exception as e:
        st.error(f"❌ 連線發生未預期的錯誤：\n`{e}`")