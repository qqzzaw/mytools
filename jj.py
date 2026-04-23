import streamlit as st
import pandas as pd
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import yfinance as yf
import qrcode
import io
import datetime
import time
import pytz

# --- 1. 页面配置 ---
st.set_page_config(page_title="GengTools™ Global", page_icon="🛠️", layout="centered")

# --- 2. 自动语言与时区感应 ---
if 'lang' not in st.session_state:
    try:
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        headers = _get_websocket_headers()
        lang_h = headers.get("Accept-Language", "en").lower()
        if "ja" in lang_h: 
            st.session_state.lang = "日本語"
            st.session_state.tz = "Asia/Tokyo"
        elif "zh" in lang_h: 
            st.session_state.lang = "简体中文"
            st.session_state.tz = "Asia/Shanghai"
        else: 
            st.session_state.lang = "English"
            st.session_state.tz = "UTC"
    except:
        st.session_state.lang = "English"
        st.session_state.tz = "UTC"

# --- 3. 侧边栏：活日历与实时时钟 ---
with st.sidebar:
    st.title("🛠️ GengTools™")
    
    # 获取感应时区的当前时间
    try:
        local_tz = pytz.timezone(st.session_state.tz)
        now = datetime.datetime.now(local_tz)
        
        # 星期适配
        week_map = {
            "English": now.strftime('%A'),
            "简体中文": "星期" + ["一","二","三","四","五","六","日"][now.weekday()],
            "日本語": ["月","火","水","木","金","土","日"][now.weekday()] + "曜日"
        }
        week_display = week_map.get(st.session_state.lang, now.strftime('%A'))

        # --- 活日历卡片设计 ---
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e1e2f 0%, #0e1117 100%); 
                        padding: 15px; border-radius: 12px; border: 1px solid #d4af37; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
                <p style="color: #d4af37; margin: 0; font-size: 0.9rem; font-weight: bold; letter-spacing: 2px;">{week_display}</p>
                <h1 style="margin: 5px 0; color: white; font-size: 2.5rem;">{now.strftime('%H:%M')}</h1>
                <p style="margin: 0; color: #fff; font-size: 1.1rem;">{now.strftime('%m月%d日') if st.session_state.lang != 'English' else now.strftime('%b %d')}</p>
                <p style="margin: 5px 0 0 0; color: #555; font-size: 0.7rem;">{st.session_state.tz} · {now.year}</p>
            </div>
        """, unsafe_allow_stdio=True)
    except:
        st.write("Calendar Syncing...")

    st.divider()
    
    # 语言选择（手动切换后会立即重绘日历）
    st.session_state.lang = st.selectbox("Language / 言語", ["English", "简体中文", "日本語"], 
                                         index=["English", "简体中文", "日本語"].index(st.session_state.lang))
    
    # 动态读取工具列表
    try:
        df_menu = pd.read_csv("tools_list.csv")
        lang_col = {"English": "name_en", "简体中文": "name_zh", "日本語": "name_ja"}[st.session_state.lang]
        options = [f"{row['icon']} {row[lang_col]}" for _, row in df_menu.iterrows() if row['id'] != 'm8']
        choice = st.radio("Global Menu", options)
        current_id = str(df_menu.iloc[options.index(choice)]['id']).lower()
    except:
        current_id = "m1"

    st.divider()
    st.link_button("🚀 Support via PayPal", "https://paypal.me", use_container_width=True)
    try: st.image("pp_pay.png", use_container_width=True)
    except: pass

# --- 4. 功能逻辑区 ---
if current_id == "m9":
    st.header("🔮 Zodiac Sign / 星座运势")
    # ... (保持星座逻辑) ...
    birthday = st.date_input("Birthday", value=datetime.date(2000, 1, 1))
    st.success("Analysis Complete! Check your daily fortune below.")

elif current_id == "m1":
    st.header("📱 QR Code Generator")
    # ... (保持二维码逻辑) ...
    text = st.text_input("URL")
    if text:
        qr_img = qrcode.make(text)
        buf = io.BytesIO(); qr_img.save(buf, format="PNG")
        st.image(buf.getvalue(), width=250)

# --- 5. 底部 ---
st.write("---")
st.code("geng-tools.streamlit.app", language="text")
st.caption("© 2024 GengTools™ | Global Service Node")
