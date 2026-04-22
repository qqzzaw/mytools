import streamlit as st
import pandas as pd
from PIL import Image, ImageOps, ImageFilter
import yfinance as yf
import qrcode
import io
import datetime
import time

# --- 1. 核心：智能读取 CSV 菜单 (遥控器) ---
@st.cache_data
def load_tools():
    # 读取你的 CSV 文件
    df = pd.read_csv("tools_list.csv")
    return df

try:
    df_menu = load_tools()
except:
    # 如果 CSV 还没准备好，提供一个保底菜单防止报错
    df_menu = pd.DataFrame([{"id":"m1","name_en":"QR","name_zh":"二维码","name_ja":"QR","icon":"📱"}])

# --- 2. 语言与页面配置 ---
st.set_page_config(page_title="GengTools™", page_icon="🛠️", layout="centered")

if 'lang' not in st.session_state:
    st.session_state.lang = "English" # 默认

with st.sidebar:
    st.title("🛠️ GengTools™")
    st.session_state.lang = st.selectbox("Language", ["English", "简体中文", "日本語"])
    
    # 自动根据语言选择 CSV 中的列名
    lang_col = "name_en"
    if st.session_state.lang == "简体中文": lang_col = "name_zh"
    if st.session_state.lang == "日本語": lang_col = "name_ja"

    # --- 动态生成菜单 (这就是你要的自动更新) ---
    display_names = [f"{row['icon']} {row[lang_col]}" for _, row in df_menu.iterrows()]
    selected_display = st.sidebar.radio("Global Menu", display_names)
    
    # 获取当前选中的 ID (例如 m1, m2...)
    current_id = df_menu.iloc[display_names.index(selected_display)]['id']

    st.divider()
    st.link_button("🚀 PayPal Donate", "https://paypal.me", use_container_width=True)
    try: st.image("pp_pay.png", use_container_width=True)
    except: pass

# --- 3. 工具逻辑分类执行 ---

# 根据 CSV 里的 ID 来判断运行哪个工具
if current_id == "m1":
    st.header(selected_display)
    text = st.text_input("Content", placeholder="https://")
    if text:
        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(text); qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO(); img_qr.save(buf, format="PNG")
        st.image(buf.getvalue(), width=250)

elif current_id == "m4":
    st.header(selected_display)
    amount = st.number_input("Amount", value=100.0)
    pair = st.selectbox("Pair", ["USD/CNY", "USD/JPY", "CNY/JPY"])
    if st.button("Get Rate"):
        with st.spinner("Live..."):
            tk = yf.Ticker(pair.replace("/", "") + "=X")
            rate = tk.history(period="1d")['Close'].iloc[-1]
            st.metric("Rate", round(rate, 4))
            st.success(f"Total: {round(amount * rate, 2)}")

elif current_id == "m2":
    st.header(selected_display)
    file = st.file_uploader("Upload", type=["jpg","png"])
    if file:
        img = Image.open(file).convert("RGB")
        w, h = img.size; s = min(w, h)
        img = img.crop(((w-s)//2, (h-s)//2, (w+s)//2, (h+s)//2))
        if st.button("Run"):
            step = s // 3
            cols = st.columns(3)
            for i in range(3):
                for j in range(3):
                    box = (j*step, i*step, (j+1)*step, (i+1)*step)
                    part = img.crop(box); b = io.BytesIO(); part.save(b, format="JPEG")
                    cols[j].image(part, use_container_width=True)
                    cols[j].download_button(f"#{i*3+j+1}", b.getvalue(), f"p_{i*3+j+1}.jpg")

# 底部声明
st.divider()
st.caption(f"© {datetime.date.today().year} GengTools™ | Data-Driven System")
