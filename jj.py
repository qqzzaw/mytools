import streamlit as st
import pandas as pd
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import yfinance as yf
import qrcode
import io
import datetime
import time

# --- 1. 页面配置与语言感应 ---
st.set_page_config(page_title="GengTools™ Global", page_icon="🛠️", layout="centered")

if 'lang' not in st.session_state:
    st.session_state.lang = "English"

# --- 2. 智能读取 CSV 菜单 ---
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

# --- 3. 侧边栏构建 ---
with st.sidebar:
    st.title("🛠️ GengTools™")
    st.session_state.lang = st.selectbox("Language", ["English", "简体中文", "日本語"])
    lang_map = {"English": "name_en", "简体中文": "name_zh", "日本語": "name_ja"}
    lang_col = lang_map[st.session_state.lang]
    
    st.divider()
    options = [f"{row['icon']} {row[lang_col]}" for _, row in df_menu.iterrows()]
    choice = st.radio("Menu", options)
    idx = options.index(choice)
    current_id = str(df_menu.iloc[idx]['id']).lower()

    st.divider()
    st.link_button("🚀 PayPal", "https://paypal.me", use_container_width=True)
    try: st.image("pp_pay.png", use_container_width=True)
    except: pass
    st.caption("🟢 Status: Live")

# --- 4. 核心功能分发 (确保逻辑不乱) ---

if current_id == "m1":
    st.header(choice)
    text = st.text_input("Content", placeholder="https://")
    if text:
        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(text); qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO(); img.save(buf, format="PNG")
        st.image(buf.getvalue(), width=250)
        st.download_button("Download", buf.getvalue(), "qr.png")

elif current_id == "m2":
    st.header(choice)
    file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    if file:
        img = Image.open(file).convert("RGB")
        w, h = img.size; s = min(w, h)
        img = img.crop(((w-s)//2, (h-s)//2, (w+s)//2, (h+s)//2))
        if st.button("Execute"):
            step = s // 3; cols = st.columns(3)
            for i in range(3):
                for j in range(3):
                    box = (j*step, i*step, (j+1)*step, (i+1)*step)
                    part = img.crop(box); b = io.BytesIO(); part.save(b, format="JPEG")
                    cols[j].image(part, use_container_width=True)
                    cols[j].download_button(f"#{i*3+j+1}", b.getvalue(), f"p_{i*3+j+1}.jpg")

elif current_id == "m3":
    st.header(choice)
    kw = st.text_input("Keyword", "Viral")
    if st.button("Generate"):
        tags = [f"#{kw}", "#fyp", "#viral", "#trending", "#foryou"]
        st.code(" ".join(tags))

elif current_id == "m4":
    st.header(choice)
    amount = st.number_input("Amount", value=100.0)
    pairs = {"USD/CNY": "CNY=X", "USD/JPY": "JPY=X", "CNY/JPY": "CNYJPY=X", "EUR/USD": "EURUSD=X"}
    pair = st.selectbox("Pair", list(pairs.keys()))
    if st.button("Get Rate"):
        with st.spinner("Loading..."):
            try:
                tk = yf.Ticker(pairs[pair])
                rate = tk.history(period="1d")['Close'].iloc[-1]
                st.metric("Live Rate", round(rate, 4))
                st.success(f"Total: {round(amount * rate, 2)}")
            except: st.error("Link Error")

elif current_id == "m5":
    st.header(choice)
    file = st.file_uploader("Image", type=["jpg", "png"])
    if file:
        img = Image.open(file).convert("RGB")
        st.image(img, caption="Original")
        if st.button("AI Fix"):
            img = ImageEnhance.Sharpness(img).enhance(2.0)
            st.image(img, caption="Enhanced")
            buf = io.BytesIO(); img.save(buf, format="JPEG")
            st.download_button("Download", buf.getvalue(), "fix.jpg")

elif current_id == "m6":
    st.header(choice)
    v_file = st.file_uploader("Upload Video", type=["mp4", "mov"])
    if v_file:
        st.video(v_file)
        st.write("File Size:", round(v_file.size / 1024 / 1024, 2), "MB")

elif current_id == "m7":
    st.header(choice)
    note = st.text_area("Notes...", height=200)
    if note:
        st.download_button("Save TXT", note, "note.txt")

# --- 5. 底部 TikTok 宣传海报 (这里是重点，不乱跑) ---
st.write("---")
st.subheader("📸 TikTok Lite Poster")

poster_html = """
<div style="background: linear-gradient(135deg, #0e1117 0%, #1a1c23 100%); 
            padding: 40px; border: 3px solid #d4af37; border-radius: 15px; text-align: center; font-family: sans-serif;">
    <h1 style="color: #d4af37; font-size: 38px; margin-bottom: 5px;">GengTools™</h1>
    <p style="color: #888; font-size: 14px;">Global Productivity Tools</p>
    <div style="text-align: left; margin: 20px auto; display: inline-block; color: white; font-size: 18px; line-height: 1.8;">
        🚀 9-Grid Photo Splitter<br>
        💹 Live Currency Exchange<br>
        📱 Pro QR Generator<br>
        ✨ AI Portrait Enhancer<br>
        🎬 Video Info Expert
    </div>
    <div style="background: rgba(212, 175, 55, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;">
        <p style="color: #d4af37; margin: 0; font-size: 12px;">OFFICIAL LINK</p>
        <h3 style="color: white; margin: 5px 0; font-size: 22px;">geng-tools.streamlit.app</h3>
    </div>
    <p style="color: #444; font-size: 12px; margin-top: 15px;">PayPal: aaa14743 | © 2024</p>
</div>
"""
st.markdown(poster_html, unsafe_allow_stdio=True)
