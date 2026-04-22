import streamlit as st
import pandas as pd
from PIL import Image, ImageOps, ImageEnhance
import datetime
import io
import time

# --- 1. 尝试导入库 ---
try:
    import yfinance as yf
except:
    yf = None
try:
    import qrcode
except:
    qrcode = None

# --- 2. 页面配置 ---
st.set_page_config(page_title="GengTools™", page_icon="🛠️", layout="centered")

if 'lang' not in st.session_state:
    st.session_state.lang = "English"

# --- 3. 读取 CSV 菜单 ---
@st.cache_data(ttl=60)
def load_config():
    try:
        df = pd.read_csv("tools_list.csv")
        df.columns = df.columns.str.strip()
        df['id'] = df['id'].astype(str).str.strip().str.lower()
        return df
    except:
        return pd.DataFrame([{"id":"m1","name_en":"QR Creator","name_zh":"二维码生成","name_ja":"QR作成","icon":"📱"}])

df_menu = load_config()

# --- 4. 侧边栏 ---
with st.sidebar:
    st.title("🛠️ GengTools™")
    st.session_state.lang = st.selectbox("Language", ["English", "简体中文", "日本語"])
    lang_map = {"English": "name_en", "简体中文": "name_zh", "日本語": "name_ja"}
    lang_col = lang_map[st.session_state.lang]
    
    st.divider()
    options = [f"{row['icon']} {row[lang_col]}" for _, row in df_menu.iterrows()]
    choice = st.sidebar.radio("Menu", options)
    idx = options.index(choice)
    current_id = str(df_menu.iloc[idx]['id']).lower()

    st.divider()
    st.link_button("🚀 Support via PayPal", "https://paypal.me", use_container_width=True)
    st.caption("🟢 System: Online")

# --- 5. 功能引擎 ---
if current_id == "m1":
    st.header(choice)
    text = st.text_input("URL / Content", placeholder="https://")
    if text and qrcode:
        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(text); qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO(); img.save(buf, format="PNG")
        st.image(buf.getvalue(), width=250)

elif current_id == "m4":
    st.header(choice)
    if yf:
        amount = st.number_input("Amount", value=100.0)
        pair = st.selectbox("Pair", ["USD/CNY", "USD/JPY", "CNY/JPY"])
        if st.button("Get Rate"):
            try:
                tk = yf.Ticker(pair.replace("/", "") + "=X")
                rate = tk.history(period="1d")['Close'].iloc[-1]
                st.metric("Rate", round(rate, 4))
            except: st.error("Market Busy")

# --- 6. 底部海报 (改用原生组件，彻底修复红屏) ---
st.write("---")
with st.container():
    # 使用 st.success 模拟金色边框卡片效果
    st.success("📸 **TikTok Lite / SNS Poster**")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("### GengTools™")
    with col2:
        st.write("🛠️ **Global Productivity Hub**")
    
    st.info("✅ 9-Grid | ✅ QR Code | ✅ Live Rate | ✅ AI Fix")
    
    st.code("geng-tools.streamlit.app", language="text")
    
    st.caption("🌍 Global Service | PayPal: aaa14743 | © 2024")
