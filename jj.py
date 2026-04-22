import streamlit as st
from PIL import Image
import random
import io
import datetime

# --- 1. 自动语言感应 (中文/英文/日语) ---
if 'lang' not in st.session_state:
    try:
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        headers = _get_websocket_headers()
        lang_h = headers.get("Accept-Language", "en").lower()
        if "ja" in lang_h: st.session_state.lang = "日本語"
        elif "zh" in lang_h: st.session_state.lang = "简体中文"
        else: st.session_state.lang = "English"
    except:
        st.session_state.lang = "English"

# --- 2. 国际化字典 ---
LANG_DATA = {
    "English": {"m1": "QR Generator", "m2": "9-Grid Cut", "m3": "TikTok Tags", "m4": "Unit Converter", "btn": "Run", "support": "☕ Support My Work"},
    "简体中文": {"m1": "二维码制作", "m2": "九宫格切图", "m3": "TikTok 标签", "m4": "单位换算", "btn": "立即执行", "support": "☕ 支持作者"},
    "日本語": {"m1": "QRコード作成", "m2": "9枚切り抜き", "m3": "TikTokタグ", "m4": "単位変換", "btn": "実行", "support": "☕ 応援する"}
}

st.set_page_config(page_title="Global Tools Pro", page_icon="🌐", layout="centered")
L = LANG_DATA[st.session_state.lang]

# --- 3. 侧边栏：PayPal 终极收款位 ---
with st.sidebar:
    st.title("🌐 Tools Center")
    st.session_state.lang = st.selectbox("Language", list(LANG_DATA.keys()), index=list(LANG_DATA.keys()).index(st.session_state.lang))
    
    st.divider()
    # 核心：PayPal 支付区域
    st.markdown(f"### {L['support']}")
    
    # 优先展示跳转按钮 (方便手机用户)
    st.link_button("🚀 Donate via PayPal", "https://paypal.me/aaa14743", use_container_width=True)
    
    st.write("Or scan QR code:")
    try:
        # 展示 PayPal 二维码 (图片请命名为 pp_pay.png 上传到 GitHub)
        st.image("pp_pay.png", caption="Scan with PayPal App", use_container_width=True)
    except:
        st.caption("PayPal QR Code Image missing in GitHub")
    
    st.divider()
    menu = st.radio("Menu", [L["m1"], L["m2"], L["m3"], L["m4"]])

# --- 4. 功能模块 ---
if menu == L["m1"]:
    st.header(f"📱 {L['m1']}")
    text = st.text_input("URL / Text", "https://tiktok.com")
    if text:
        qr_api = f"https://qrserver.com{text}"
        st.image(qr_api, width=250)
        st.caption("Scan or long press to save.")

elif menu == L["m2"]:
    st.header(f"🧩 {L['m2']}")
    file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    if file:
        img = Image.open(file)
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
                    part.save(buf, format="JPEG")
                    cols[j].image(part, use_container_width=True)
                    cols[j].download_button(f"#{i*3+j+1}", buf.getvalue(), f"p_{i*3+j+1}.jpg")

elif menu == L["m3"]:
    st.header(f"🔥 {L['m3']}")
    kw = st.text_input("Keyword", "Viral")
    if st.button(L["btn"]):
        tags = [f"#{kw}", "#fyp", "#trending", "#viral", "#foryou"]
        st.code(" ".join(tags))
        st.success("Copied!")

elif menu == L["m4"]:
    st.header(f"⚖️ {L['m4']}")
    val = st.number_input("Value", value=1.0)
    u_type = st.selectbox("Type", ["KM to Miles", "KG to Lbs", "C to F"])
    if u_type == "KM to Miles": st.metric("Result", f"{round(val*0.621, 2)} mi")
    elif u_type == "KG to Lbs": st.metric("Result", f"{round(val*2.204, 2)} lbs")
    elif u_type == "C to F": st.metric("Result", f"{round(val*1.8+32, 2)} °F")

st.divider()
st.caption(f"© {datetime.date.today().year} Global Tools | PayPal: aaa14743")
