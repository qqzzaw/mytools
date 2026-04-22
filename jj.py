import streamlit as st
import pandas as pd
from PIL import Image, ImageOps, ImageFilter
import yfinance as yf
import qrcode
import io
import datetime
import time

# --- 1. 性能优化：极速读取 CSV 菜单 ---
@st.cache_data(ttl=3600) # 缓存1小时，极大提升全球用户的打开速度
def load_tools_config():
    try:
        df = pd.read_csv("tools_list.csv")
        return df
    except:
        # 保底逻辑：如果 CSV 损坏或缺失，确保网站不崩
        return pd.DataFrame([
            {"id":"m1","name_en":"QR Creator","name_zh":"二维码生成","name_ja":"QR作成","icon":"📱"},
            {"id":"m4","name_en":"Live Rate","name_zh":"实时汇率","name_ja":"為替レート","icon":"💱"}
        ])

# --- 2. 自动语言感应 (适配 TikTok 全球流量) ---
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

# --- 3. 页面配置与 UI 优化 ---
st.set_page_config(page_title="GengTools™", page_icon="🛠️", layout="centered")

# 读取配置
df_menu = load_tools_config()

with st.sidebar:
    st.title("🛠️ GengTools™")
    st.session_state.lang = st.selectbox("Language / 言語", ["English", "简体中文", "日本語"], 
                                         index=["English", "简体中文", "日本語"].index(st.session_state.lang))
    
    # 动态匹配 CSV 中的语言列
    lang_col = {"English": "name_en", "简体中文": "name_zh", "日本語": "name_ja"}[st.session_state.lang]
    
    st.divider()
    # 动态侧边栏菜单：直接关联 CSV
    menu_options = [f"{row['icon']} {row[lang_col]}" for _, row in df_menu.iterrows()]
    choice = st.radio("Global Menu", menu_options)
    current_id = df_menu.iloc[menu_options.index(choice)]['id']

    st.divider()
    # 国际收款位
    st.markdown("### ☕ Support Me")
    st.link_button("🚀 Donate via PayPal", "https://paypal.me", use_container_width=True)
    try:
        st.image("pp_pay.png", caption="PayPal QR Code", use_container_width=True)
    except:
        st.caption("QR Ready")
    
    st.caption(f"🟢 System: Online | {datetime.date.today()}")

# --- 4. 工具模块核心逻辑 (优化处理效率) ---

# 工具 m1: 二维码 (本地极速引擎)
if current_id == "m1":
    st.header(choice)
    text = st.text_input("URL / Content", placeholder="https://tiktok.com")
    if text:
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(text); qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO(); img_qr.save(buf, format="PNG")
        st.image(buf.getvalue(), width=250)
        st.download_button("Download QR", buf.getvalue(), "gengtools_qr.png")

# 工具 m4: 实时汇率 (接入雅虎财经实时数据)
elif current_id == "m4":
    st.header(choice)
    amount = st.number_input("Amount", value=100.0)
    pairs = {"USD/CNY": "CNY=X", "USD/JPY": "JPY=X", "CNY/JPY": "CNYJPY=X", "EUR/USD": "EURUSD=X"}
    pair = st.selectbox("Currency Pair", list(pairs.keys()))
    if st.button("Get Real-time Rate"):
        with st.spinner("Connecting to Market..."):
            try:
                tk = yf.Ticker(pairs[pair])
                rate = tk.history(period="1d")['Close'].iloc[-1]
                st.metric(f"1 {pair.split('/')[0]} =", f"{round(rate, 4)}")
                st.success(f"Total: {round(amount * rate, 2)}")
            except:
                st.error("Connection Timeout. Please retry.")

# 工具 m2: 九宫格 (处理大图不卡顿)
elif current_id == "m2":
    st.header(choice)
    file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    if file:
        img = Image.open(file).convert("RGB")
        img = ImageOps.exif_transpose(img)
        w, h = img.size; s = min(w, h)
        img = img.crop(((w-s)//2, (h-s)//2, (w+s)//2, (h+s)//2))
        if st.button("Process"):
            step = s // 3
            cols = st.columns(3)
            for i in range(3):
                for j in range(3):
                    box = (j*step, i*step, (j+1)*step, (i+1)*step)
                    part = img.crop(box)
                    b = io.BytesIO(); part.save(b, format="JPEG", quality=90)
                    cols[j].image(part, use_container_width=True)
                    cols[j].download_button(f"#{i*3+j+1}", b.getvalue(), f"p_{i*3+j+1}.jpg")

# 其他工具模块按需延续...
else:
    st.info("System evolving... This module will be active soon via CSV update.")

st.divider()
st.caption(f"© {datetime.date.today().year} GengTools™ Global | Data-Driven Utilities")
