import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 設定網頁標題
st.title("📱 我的隨身資料記錄器")

# 1. 自動初始化輕量雲端資料庫
@st.cache_resource
def get_connection():
    # 建立一個名為 my_notes.db 的資料庫
    conn = sqlite3.connect("my_notes.db", check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    return conn

conn = get_connection()
cursor = conn.cursor()

# 2. 手機輸入介面
with st.form("note_form", clear_on_submit=True):
    user_input = st.text_area("輸入要記錄的內容：")
    submitted = st.form_submit_button("儲存記錄")
    
    if submitted and user_input.strip():
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute("INSERT INTO notes (time, content) VALUES (?, ?)", (current_time, user_input))
        conn.commit()
        st.success("✅ 記錄成功儲存！")

st.divider()

# 3. 隨時查看歷史記錄
st.subheader("📋 歷史記錄清單")
if st.button("重新整理 / 查看資料"):
    df = pd.read_sql("SELECT time AS 時間, content AS 記錄內容 FROM notes ORDER BY id DESC", conn)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("目前還沒有任何記錄。")