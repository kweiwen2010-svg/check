import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json

st.title("🔍 Google Sheets 連線自我檢查")

sheet_name = st.text_input("輸入你的 Google Sheet 名稱", value="你的_Google_Sheet_名稱")

st.subheader("1. 檢查 Secrets 設定")

# 支援 dict 或直接讀取整串 json 字串，自動處理換行格式
try:
    if "gcp_service_account" in st.secrets:
        raw_secret = st.secrets["gcp_service_account"]
        if isinstance(raw_secret, str):
            creds_dict = json.loads(raw_secret)
        else:
            creds_dict = dict(raw_secret)
            
        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ],
        )
        st.success("✅ Service Account 憑證格式正確！")
        st.info(f"服務帳號 Email: `{creds.service_account_email}`")
        st.warning(f"⚠️ 請務必確認你的 Google Sheet 已經分享（共用）給這個 Email：\n`{creds.service_account_email}`")
    else:
        st.error("❌ 找不到 `gcp_service_account`！")
        st.stop()
except Exception as e:
    st.error(f"❌ 憑證解析失敗：\n`{e}`")
    st.stop()

# 2. 測試實際讀取 Google Sheet
st.subheader("2. 測試連線與讀取")
if st.button("開始測試讀取"):
    try:
        client = gspread.authorize(creds)
        sh = client.open(sheet_name)
        st.success(f"🎉 成功連線並開啟試算表：`{sheet_name}`")
        
        worksheet = sh.get_worksheet(0)
        data = worksheet.get_all_records()
        st.write(f"✅ 成功讀取資料！目前工作表名稱：`{worksheet.title}`")
        st.json(data[:3])
        
    except gspread.exceptions.SpreadsheetNotFound:
        st.error(f"❌ 找不到名為 `{sheet_name}` 的試算表。請確認名稱是否完全正確，且已分享給服務帳號。")
    except Exception as e:
        st.error(f"❌ 連線發生未預期的錯誤：\n`{e}`")