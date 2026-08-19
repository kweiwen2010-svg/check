import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# 1. 頁面標題
st.title("Google Sheets 連線測試")

# 2. 定義憑證處理函數
def get_gspread_client():
    try:
        # 從 st.secrets 取得設定
        creds_dict = dict(st.secrets["gcp_service_account"])
        
        # 關鍵修正：確保 private_key 中的 "\n" 字串被正確轉換為換行符號
        # 這能解決編輯器自動折行導致的憑證解析錯誤
        if "private_key" in creds_dict:
            creds_dict["private_key"] = creds_dict["private_key"].replace(r"\n", "\n")
        
        # 定義權限範圍
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        
        # 建立憑證物件
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        
        # 授權 gspread
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"憑證載入失敗: {e}")
        return None

# 3. 測試讀取功能
if st.button("開始測試連線"):
    client = get_gspread_client()
    
    if client:
        st.success("✅ 憑證載入成功，正在嘗試存取試算表...")
        
        try:
            # 這裡請替換成你想測試的試算表名稱
            # 記得要在該試算表中，將 service account email 加入共用權限
            spreadsheet = client.open("你的試算表名稱")
            worksheet = spreadsheet.sheet1
            data = worksheet.get_all_values()
            
            st.write("成功讀取到資料！")
            st.dataframe(data)
        except Exception as e:
            st.error(f"無法開啟試算表，請確認共用權限是否已加入: {e}")
            st.info("請將此 Email 加入共用: " + st.secrets["gcp_service_account"]["client_email"])