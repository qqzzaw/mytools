import streamlit as st
from PIL import Image, ImageOps, ImageFilter
import yfinance as yf
import qrcode
import io
import datetime
import time
import random

# --- 1. 自动语言感应 (Silent Detect) ---
if 'lang' not in st.session_state:
    try:
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        headers = _get_websocket_headers()
        lang_h = headers.get("Accept-Language", "en").lower()
        if "ja" in lang_h: st.session_state.lang = "日本語 🇯🇵"
        elif "zh" in lang_h: st.session_state.lang = "简体中文 🇨🇳"
        elif "es" in lang_h: st.session_state.lang = "Español 🇪🇸"
        elif "fr" in lang_h: st.session_state.lang = "Français 🇫🇷"
        else: st.session_state.lang = "English 🇺🇸"
    except:
        st.session_state.lang = "English 🇺🇸"

# --- 2. 全球化字典 (V4.0 视觉增强版) ---
LANG_DATA = {
    "English 🇺🇸": {
        "m1": "QR Generator", "m2": "9-Grid Pro", "m3": "Viral Tags", 
        "m4": "Live Currency", "m5": "AI Photo Fix", "btn": "Generate", "support": "Support Me"
    },
    "简体中文 🇨🇳": {
        "m1": "二维码制作", "m2": "九宫格切图", "m3": "热门标签", 
        "m4": "实时汇率", "m5": "AI 人像优化", "btn": "立即生成", "support": "支持作者"
    },
    "日本語 🇯🇵": {
        "m1": "QR作成", "m2": "9枚切り抜き", "m3": "TikTokタグ", 
        "m4": "為替レート", "m5": "AI写真加工", "btn": "実行", "support": "応援する"
    },
    "Español 🇪🇸": {"m1": "QR", "m2": "Corte 9", "m3": "Tags", "m4": "Divisas", "m5": "AI Foto", "btn": "Ejecutar", "support": "Soportar"},
    "Français 🇫🇷": {"m1": "QR", "m2": "Coupe 9", "m3": "Tags", "m4": "Devises", "m5": "AI Photo", "btn": "Exécuter", "support": "Soutenir"}
}

st.set_page_config(page_title="GengTools™ Global", page_icon="⚡", layout="centered")
L = LANG_DATA[st.session_state.lang]

# --- 3. 侧边栏：国际收银台 ---
with st.sidebar:
    st.title("🛠️ GengTools™")
    st.session_state.lang = st.selectbox("Language / 语言", list(LANG_DATA.keys()), index=list(LANG_DATA.keys()).index(st.session_state.lang))
    
    st.divider()
    st.markdown(f"**{L['support']}**")
    st.link_button("🚀 PayPal.Me (aaa14743)", "https://paypal.me", use_container_width=True)
    try: st.image("pp_pay.png", caption="PayPal QR", use_container_width=True)
    except: st.caption("Donation Link Ready")
    
    st.divider()
    menu = st.radio("Global Tools", [L["m1"], L["m2"], L["m3"], L["m4"], L["m5"]])
    st.caption("🟢 Status: Optimized for TikTok")

# --- 4. 功能模块 ---

# 工具 1：二维码 (本地生成)
if menu == L["m1"]:
    st.header(L["m1"])
    text = st.text_input("URL / Content", placeholder="https://tiktok.com")
    if text:
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(text)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO()
        img_qr.save(buf, format="PNG")
        st.image(buf.getvalue(), width=250)
        st.download_button("Download", buf.getvalue(), "geng_qr.png")

# 工具 5：AI 人像/照片优化 (新上线功能)
elif menu == L["m5"]:
    st.header(L["m5"])
    file = st.file_uploader("Upload Photo", type=["jpg", "png", "jpeg"])
    if file:
        img = Image.open(file).convert("RGB")
        img = ImageOps.exif_transpose(img)
        st.image(img, caption="Original", use_container_width=True)
        
        mode = st.radio("Optimization Mode", ["Auto-Beauty (一键美颜)", "Background Blur (背景虚化)"])
        
        if st.button(L["btn"], use_container_width=True):
            with st.spinner("AI Processing..."):
                time.sleep(1.2)
                if "Beauty" in mode:
                    # 美颜逻辑：提升亮度、对比度，稍微柔化
                    img = ImageOps.autocontrast(img, cutoff=2)
                    img = img.filter(ImageFilter.SMOOTH_MORE)
                else:
                    # 虚化逻辑：模拟大光圈
                    img = img.filter(ImageFilter.GaussianBlur(radius=4))
                
                st.success("Analysis Complete!")
                st.image(img, caption="Enhanced Result", use_container_width=True)
                
                buf = io.BytesIO()
                img.save(buf, format="JPEG", quality=95)
                st.download_button("Download HD Result", buf.getvalue(), "geng_ai_fixed.jpg")

# 工具 4：汇率 (实时联网)
elif menu == L["m4"]:
    st.header(L["m4"])
    amount = st.number_input("Value", value=100.0)
    pairs = {"USD/CNY": "CNY=X", "USD/JPY": "JPY=X", "EUR/USD": "EURUSD=X", "CNY/JPY": "CNYJPY=X"}
    pair = st.selectbox("Currency Pair", list(pairs.keys()))
    if st.button(L["btn"]):
        with st.spinner("Live Syncing..."):
            try:
                ticker = yf.Ticker(pairs[pair])
                rate = ticker.fast_info['last_price']
                st.metric(f"Rate", f"{round(rate, 4)}")
                st.success(f"Total: {round(amount * rate, 2)}")
            except: st.error("Market Link Busy")

# 工具 2：九宫格
elif menu == L["m2"]:
    st.header(L["m2"])
    file = st.file_uploader("Upload", type=["jpg", "png", "jpeg"])
    if file:
        img = Image.open(file).convert("RGB")
        img = ImageOps.exif_transpose(img)
        w, h = img.size
        size = min(w, h)
        img = img.crop(((w-size)//2, (h-size)//2, (w+size)//2, (h+size)//2))
        if st.button(L["btn"]):
            step = size // 3
            cols = st.columns(3)
            for i in range(3):
                for j in range(3):
                    box = (j*step, i*step, (j+1)*step, (i+1)*step)
                    part = img.crop(box)
                    buf = io.BytesIO()
                    part.save(buf, format="JPEG", quality=90)
                    cols[j].image(part, use_container_width=True)
                    cols[j].download_button(f"#{i*3+j+1}", buf.getvalue(), f"p_{i*3+j+1}.jpg")

# 工具 3：智能标签矩阵
elif menu == L["m3"]:
    st.header(L["m3"])
    kw = st.text_input("Topic", "Viral")
    if st.button(L["btn"]):
        tags = [f"#{kw}", f"#{kw}hacks", "#fyp", "#viral", "#trending", "#useful", "#tools", "#2024"]
        random.shuffle(tags)
        st.code(" ".join(tags))

st.divider()
st.caption(f"© {datetime.date.today().year} GengTools™ Global | TikTok Professional Utilities")
