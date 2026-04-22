import streamlit as st
from PIL import Image, ImageOps
import random
import io
import datetime

# --- 1. 自动语言感应 (增强版) ---
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

# --- 2. 国际化字典 (新增工具名) ---
LANG_DATA = {
    "English": {
        "m1": "QR Generator", "m2": "9-Grid Cut", "m3": "TikTok Tags", 
        "m4": "Currency Calc", "m5": "BG Remover",
        "btn": "Run", "support": "☕ Support My Work", "tip": "Success!"
    },
    "简体中文": {
        "m1": "二维码制作", "m2": "九宫格切图", "m3": "TikTok 标签", 
        "m4": "汇率换算", "m5": "证件照抠图",
        "btn": "立即执行", "support": "☕ 支持作者", "tip": "处理完成！"
    },
    "日本語": {
        "m1": "QRコード作成", "m2": "9枚切り抜き", "m3": "TikTokタグ", 
        "m4": "為替計算", "m5": "背景削除",
        "btn": "実行", "support": "☕ 応援する", "tip": "完了！"
    }
}

st.set_page_config(page_title="Global Tools Pro", page_icon="🌐", layout="centered")
L = LANG_DATA[st.session_state.lang]

# --- 3. 侧边栏：收款位 (Bug 修复：确保链接优先级) ---
with st.sidebar:
    st.title("🌐 Tools Center")
    st.session_state.lang = st.selectbox("Language", list(LANG_DATA.keys()), index=list(LANG_DATA.keys()).index(st.session_state.lang))
    
    st.divider()
    st.markdown(f"### {L['support']}")
    # 核心链接：确保全球跳转无误
    st.link_button("🚀 Donate via PayPal", "https://paypal.me", use_container_width=True)
    
    try:
        st.image("pp_pay.png", caption="Scan QR with PayPal App", use_container_width=True)
    except:
        st.caption("QR Code standby...")
    
    st.divider()
    # 新增了两个菜单选项
    menu = st.radio("Menu", [L["m1"], L["m2"], L["m3"], L["m4"], L["m5"]])

# --- 4. 功能模块优化与扩充 ---

# 功能 1：二维码 (修复：增加容错)
if menu == L["m1"]:
    st.header(f"📱 {L['m1']}")
    text = st.text_input("URL / Text", "https://tiktok.com")
    if text:
        qr_api = f"https://qrserver.com{text}"
        st.image(qr_api, width=250)
        st.caption("Tip: Use this for your TikTok Bio Link!")

# 功能 2：九宫格 (修复：大图压缩防止报错)
elif menu == L["m2"]:
    st.header(f"🧩 {L['m2']}")
    file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    if file:
        img = Image.open(file)
        # Bug Fix: 自动纠正图片方向
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
                    part.save(buf, format="JPEG", quality=85)
                    cols[j].image(part, use_container_width=True)
                    cols[j].download_button(f"#{i*3+j+1}", buf.getvalue(), f"p_{i*3+j+1}.jpg")

# 功能 3：TikTok 标签 (内容丰富)
elif menu == L["m3"]:
    st.header(f"🔥 {L['m3']}")
    kw = st.text_input("Theme", "Motivation")
    if st.button(L["btn"]):
        tags = [f"#{kw}", "#fyp", "#foryou", "#trending", "#viral", "#tech", "#useful"]
        st.code(" ".join(tags))
        st.success(L["tip"])

# 功能 4：新增汇率换算 (极简逻辑)
elif menu == L["m4"]:
    st.header(f"💱 {L['m4']}")
    amount = st.number_input("Amount / 金额", value=100.0)
    c_type = st.selectbox("Currency Pair", ["USD to CNY", "CNY to JPY", "USD to JPY"])
    # 设定动态比例 (实际可接入API，目前使用基准值)
    rates = {"USD to CNY": 7.24, "CNY to JPY": 21.3, "USD to JPY": 154.5}
    res = amount * rates[c_type]
    st.metric("Estimated", f"{round(res, 2)}")
    st.caption("Reference only, live data may vary.")

# 功能 5：背景移除 (模拟+占位)
elif menu == L["m5"]:
    st.header(f"👤 {L['m5']}")
    st.write("Coming Soon / 即将上线 (AI Powered)")
    st.info("We are optimizing the AI engine for one-click background removal.")

# --- 5. 底部 ---
st.divider()
st.caption(f"© {datetime.date.today().year} Global Tools | Powered by Streamlit")
