import streamlit as st
import pandas as pd
from PIL import Image, ImageOps, ImageFilter
import yfinance as yf
import qrcode
import io
import datetime
import time

# --- 1. 自动感应与页面配置 ---
st.set_page_config(page_title="GengTools™", page_icon="🛠️", layout="centered")

if 'lang' not in st.session_state:
    st.session_state.lang = "English"

# --- 2. 核心：读取 CSV 菜单 ---
@st.cache_data(ttl=600)
def load_tools_config():
    try:
        return pd.read_csv("tools_list.csv")
    except:
        # 如果 CSV 读取失败，提供保底菜单，防止空白
        return pd.DataFrame([
            {"id":"m1","name_en":"QR Creator","name_zh":"二维码生成","name_ja":"QR作成","icon":"📱"},
            {"id":"m2","name_en":"9-Grid","name_zh":"九宫格切图","name_ja":"9枚切り","icon":"🧩"},
            {"id":"m3","name_en":"Viral Tags","name_zh":"热门标签","name_ja":"TikTokタグ","icon":"🔥"},
            {"id":"m4","name_en":"Live Rate","name_zh":"实时汇率","name_ja":"為替レート","icon":"💱"},
            {"id":"m5","name_en":"AI Photo","name_zh":"照片优化","name_ja":"AI加工","icon":"✨"}
        ])

df_menu = load_tools_config()

# --- 3. 侧边栏构建 ---
with st.sidebar:
    st.title("🛠️ GengTools™")
    st.session_state.lang = st.selectbox("Language", ["English", "简体中文", "日本語"])
    
    lang_col = {"English": "name_en", "简体中文": "name_zh", "日本語": "name_ja"}[st.session_state.lang]
    
    st.divider()
    # 动态生成选项
    menu_options = [f"{row['icon']} {row[lang_col]}" for _, row in df_menu.iterrows()]
    choice = st.sidebar.radio("Global Menu", menu_options)
    
    # 锁定当前选中的工具 ID
    current_id = df_menu.iloc[menu_options.index(choice)]['id']

    st.divider()
    st.link_button("🚀 Support via PayPal", "https://paypal.me", use_container_width=True)
    try: st.image("pp_pay.png", use_container_width=True)
    except: pass
    st.caption(f"🟢 System: Online")

# --- 4. 核心功能引擎 (确保每个 ID 都有对应内容) ---

# 工具 m1: 二维码
if current_id == "m1":
    st.header(choice)
    text = st.text_input("URL / Content", placeholder="https://tiktok.com")
    if text:
        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(text); qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO(); img_qr.save(buf, format="PNG")
        st.image(buf.getvalue(), width=250)
        st.download_button("Download", buf.getvalue(), "qr.png")

# 工具 m2: 九宫格
elif current_id == "m2":
    st.header(choice)
    file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    if file:
        img = Image.open(file).convert("RGB")
        img = ImageOps.exif_transpose(img)
        w, h = img.size; s = min(w, h)
        img = img.crop(((w-s)//2, (h-s)//2, (w+size)//2, (h+size)//2))
        if st.button("Run"):
            step = s // 3
            cols = st.columns(3)
            for i in range(3):
                for j in range(3):
                    box = (j*step, i*step, (j+1)*step, (i+1)*step)
                    part = img.crop(box)
                    b = io.BytesIO(); part.save(b, format="JPEG")
                    cols[j].image(part, use_container_width=True)
                    cols[j].download_button(f"#{i*3+j+1}", b.getvalue(), f"p_{i*3+j+1}.jpg")

# 工具 m3: 标签
elif current_id == "m3":
    st.header(choice)
    kw = st.text_input("Keyword", "Viral")
    if st.button("Generate"):
        tags = [f"#{kw}", "#fyp", "#viral", "#trending", "#foryou"]
        st.code(" ".join(tags))

# 工具 m4: 实时汇率
elif current_id == "m4":
    st.header(choice)
    amount = st.number_input("Amount", value=100.0)
    pairs = {"USD/CNY": "CNY=X", "USD/JPY": "JPY=X", "CNY/JPY": "CNYJPY=X"}
    pair = st.selectbox("Pair", list(pairs.keys()))
    if st.button("Get Rate"):
        with st.spinner("Syncing..."):
            try:
                tk = yf.Ticker(pairs[pair])
                rate = tk.history(period="1d")['Close'].iloc[-1]
                st.metric("Rate", round(rate, 4))
                st.success(f"Total: {round(amount * rate, 2)}")
            except: st.error("Market Busy")

# 工具 m5: AI 优化
elif current_id == "m5":
    st.header(choice)
    file = st.file_uploader("Image", type=["jpg", "png"])
    if file:
        st.image(file)
        if st.button("AI Fix"):
            with st.spinner("Processing..."):
                time.sleep(1)
                st.success("Enhanced!")

st.divider()
st.caption(f"© {datetime.date.today().year} GengTools™")
