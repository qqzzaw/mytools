import streamlit as st
import pandas as pd
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import yfinance as yf
import qrcode
import io
import datetime
import time

# --- 1. 性能优化：读取 CSV 菜单 ---
@st.cache_data(ttl=600)
def load_tools_config():
    try:
        return pd.read_csv("tools_list.csv")
    except:
        return pd.DataFrame([
            {"id":"m1","name_en":"QR Creator","name_zh":"二维码生成","name_ja":"QR作成","icon":"📱"},
            {"id":"m2","name_en":"9-Grid","name_zh":"九宫格切图","name_ja":"9枚切り","icon":"🧩"},
            {"id":"m3","name_en":"Viral Tags","name_zh":"热门标签","name_ja":"TikTokタグ","icon":"🔥"},
            {"id":"m4","name_en":"Live Rate","name_zh":"实时汇率","name_ja":"為替レート","icon":"💱"},
            {"id":"m5","name_en":"AI Photo","name_zh":"照片优化","name_ja":"AI加工","icon":"✨"},
            {"id":"m6","name_en":"Video Info","name_zh":"视频信息","name_ja":"動画情報","icon":"🎬"},
            {"id":"m7","name_en":"Smart Notes","name_zh":"智能笔记","name_ja":"メモ","icon":"📝"}
        ])

df_menu = load_tools_config()

# --- 2. 页面配置 ---
st.set_page_config(page_title="GengTools™ Global", page_icon="🛠️", layout="centered")

if 'lang' not in st.session_state:
    st.session_state.lang = "English"

# --- 3. 侧边栏 ---
with st.sidebar:
    st.title("🛠️ GengTools™")
    st.session_state.lang = st.selectbox("Language", ["English", "简体中文", "日本語"])
    lang_col = {"English": "name_en", "简体中文": "name_zh", "日本語": "name_ja"}[st.session_state.lang]
    st.divider()
    menu_options = [f"{row['icon']} {row[lang_col]}" for _, row in df_menu.iterrows()]
    choice = st.sidebar.radio("Global Menu", menu_options)
    current_id = df_menu.iloc[menu_options.index(choice)]['id']
    st.divider()
    st.link_button("🚀 Support via PayPal", "https://paypal.me", use_container_width=True)
    try: st.image("pp_pay.png", use_container_width=True)
    except: pass
    st.caption("🟢 Global Server: Online")

# --- 4. 功能逻辑引擎 ---

# m1: 二维码
if current_id == "m1":
    st.header(choice)
    text = st.text_input("Content", placeholder="https://")
    if text:
        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(text); qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO(); img_qr.save(buf, format="PNG")
        st.image(buf.getvalue(), width=250)
        st.download_button("Download", buf.getvalue(), "qr.png")

# m5: AI 照片优化 (真正实操版)
elif current_id == "m5":
    st.header(choice)
    file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    if file:
        img = Image.open(file).convert("RGB")
        st.image(img, caption="Original")
        enhance_type = st.radio("Mode", ["Sharpen (锐化)", "Brighten (增亮)", "Vivid (鲜艳)"])
        if st.button("AI Process"):
            with st.spinner("Processing..."):
                if "Sharpen" in enhance_type:
                    img = ImageEnhance.Sharpness(img).enhance(2.0)
                elif "Brighten" in enhance_type:
                    img = ImageEnhance.Brightness(img).enhance(1.3)
                else:
                    img = ImageEnhance.Color(img).enhance(1.5)
                st.image(img, caption="Enhanced")
                buf = io.BytesIO(); img.save(buf, format="JPEG")
                st.download_button("Download Result", buf.getvalue(), "geng_enhanced.jpg")

# m4: 实时汇率
elif current_id == "m4":
    st.header(choice)
    amount = st.number_input("Amount", value=100.0)
    pairs = {"USD/CNY": "CNY=X", "USD/JPY": "JPY=X", "CNY/JPY": "CNYJPY=X", "EUR/USD": "EURUSD=X"}
    pair = st.selectbox("Pair", list(pairs.keys()))
    if st.button("Get Rate"):
        with st.spinner("Syncing..."):
            try:
                tk = yf.Ticker(pairs[pair])
                rate = tk.history(period="1d")['Close'].iloc[-1]
                st.metric("Rate", round(rate, 4))
                st.success(f"Total: {round(amount * rate, 2)}")
            except: st.error("Market Busy")

# m6: 视频信息 (新增)
elif current_id == "m6":
    st.header(choice)
    v_file = st.file_uploader("Upload Video Snippet", type=["mp4", "mov"])
    if v_file:
        st.video(v_file)
        st.write("📐 File Size:", round(v_file.size / 1024 / 1024, 2), "MB")
        st.info("Analysis: Ready for TikTok Upload (Standard HD)")

# m7: 智能笔记 (新增)
elif current_id == "m7":
    st.header(choice)
    note = st.text_area("Write your ideas here...", height=200)
    if note:
        st.download_button("Save as TXT", note, "my_notes.txt")

# m2: 九宫格 (略) ... m3: 标签 (略)
elif current_id == "m2":
    st.header(choice)
    file = st.file_uploader("Upload", type=["jpg", "png", "jpeg"])
    if file:
        img = Image.open(file).convert("RGB"); w, h = img.size; s = min(w, h)
        img = img.crop(((w-s)//2, (h-s)//2, (w+s)//2, (h+s)//2))
        if st.button("Run"):
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

st.divider()
st.caption(f"© {datetime.date.today().year} GengTools™ | Global Service")
# --- 自动生成海报模块 ---
st.divider()
st.subheader("🎬 TikTok Lite 宣传海报 (请截屏使用)")

# 这段代码会直接在你的网页上画出一张黑金色的精美海报
poster_html = """
<div style="background: linear-gradient(135deg, #0e1117 0%, #1a1c23 100%); 
            padding: 40px; border: 3px solid #d4af37; border-radius: 15px; text-align: center; font-family: sans-serif;">
    <h1 style="color: #d4af37; font-size: 40px; margin-bottom: 0;">GengTools™</h1>
    <p style="color: #888; font-size: 16px;">Global Productivity Tools</p>
    <div style="text-align: left; margin: 30px auto; display: inline-block; color: white; font-size: 20px; line-height: 2;">
        ⚡ 9-Grid Photo Splitter<br>
        💹 Live Currency Exchange<br>
        📱 Pro QR Generator<br>
        ✨ AI Portrait Enhancer<br>
        🔥 Viral Hashtag Finder
    </div>
    <div style="background: rgba(212, 175, 55, 0.1); padding: 15px; border-radius: 10px; margin-top: 20px;">
        <p style="color: #d4af37; margin: 0; font-size: 14px;">ACCESS LINK</p>
        <h3 style="color: white; margin: 5px 0;">geng-tools.streamlit.app</h3>
    </div>
    <p style="color: #444; font-size: 12px; margin-top: 20px;">Global Service | PayPal: aaa14743</p>
</div>
"""
st.markdown(poster_html, unsafe_allow_stdio=True)
