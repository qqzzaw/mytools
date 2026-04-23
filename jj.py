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

# --- 2. 自动感应逻辑 (实时时区) ---
if 'lang' not in st.session_state:
    try:
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        headers = _get_websocket_headers()
        lang_h = headers.get("Accept-Language", "en").lower()
        if "ja" in lang_h: 
            st.session_state.lang = "日本語"; st.session_state.tz = "Asia/Tokyo"
        elif "zh" in lang_h: 
            st.session_state.lang = "简体中文"; st.session_state.tz = "Asia/Shanghai"
        else: 
            st.session_state.lang = "English"; st.session_state.tz = "UTC"
    except:
        st.session_state.lang = "English"; st.session_state.tz = "UTC"

# --- 3. 侧边栏：核心展示 (修复时间不显示问题) ---
with st.sidebar:
    st.title("🛠️ GengTools™")
    
    # --- 强力时间日历模块 (放在这里绝对能看到) ---
    try:
        # 获取实时感应的时间
        target_tz = pytz.timezone(st.session_state.tz)
        now_dt = datetime.datetime.now(target_tz)
        
        # 星期适配
        week_map = {
            "English": now_dt.strftime('%A'),
            "简体中文": "星期" + ["一","二","三","四","五","六","日"][now_dt.weekday()],
            "日本語": ["月","火","水","木","金","土","日"][now_dt.weekday()] + "曜日"
        }
        week_str = week_map.get(st.session_state.lang, now_dt.strftime('%A'))

        # 渲染黑金日历卡片
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e1e2f 0%, #0e1117 100%); 
                        padding: 15px; border-radius: 12px; border: 1px solid #d4af37; text-align: center; margin-bottom: 20px;">
                <p style="color: #d4af37; margin: 0; font-weight: bold; font-size: 0.9rem;">{week_str}</p>
                <h1 style="margin: 5px 0; color: white; font-size: 2.2rem;">{now_dt.strftime('%H:%M')}</h1>
                <p style="margin: 0; color: #fff; font-size: 1rem;">{now_dt.strftime('%m月%d日') if st.session_state.lang != 'English' else now_dt.strftime('%b %d')}</p>
                <p style="margin: 5px 0 0 0; color: #555; font-size: 0.7rem;">{st.session_state.tz} · {now_dt.year}</p>
            </div>
        """, unsafe_allow_stdio=True)
    except Exception as e:
        st.caption(f"Time Syncing... {e}")

    st.divider()
    
    # 语言选择
    st.session_state.lang = st.selectbox("Language / 言語", ["English", "简体中文", "日本語"], 
                                         index=["English", "简体中文", "日本語"].index(st.session_state.lang))
    
    # 动态菜单读取
    try:
        df_menu = pd.read_csv("tools_list.csv")
        df_menu.columns = df_menu.columns.str.strip()
        df_menu['id'] = df_menu['id'].astype(str).str.strip().str.lower()
        lang_col = {"English": "name_en", "简体中文": "name_zh", "日本語": "name_ja"}[st.session_state.lang]
        options = [f"{row['icon']} {row[lang_col]}" for _, row in df_menu.iterrows() if row['id'] != 'm8']
        choice = st.radio("Menu", options)
        current_id = str(df_menu.iloc[options.index(choice)]['id']).lower()
    except:
        current_id = "m1"
        st.error("CSV Menu Error")

    st.divider()
    st.link_button("🚀 Support via PayPal", "https://paypal.me", use_container_width=True)
    try: st.image("pp_pay.png", use_container_width=True)
    except: pass

# --- 4. 核心功能分发 (所有功能逻辑保留) ---

if current_id == "m1":
    st.header(choice)
    text = st.text_input("Content", placeholder="https://")
    if text:
        qr_img = qrcode.make(text)
        buf = io.BytesIO(); qr_img.save(buf, format="PNG")
        st.image(buf.getvalue(), width=250)
        st.download_button("Download", buf.getvalue(), "qr.png")

elif current_id == "m2":
    st.header(choice)
    file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    if file:
        img = Image.open(file).convert("RGB")
        img = ImageOps.exif_transpose(img)
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
        with st.spinner("Syncing..."):
            try:
                tk = yf.Ticker(pairs[pair])
                rate = tk.history(period="1d")['Close'].iloc[-1]
                st.metric("Live Rate", round(rate, 4))
                st.success(f"Total: {round(amount * rate, 2)}")
            except: st.error("Market Busy")

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
    v_file = st.file_uploader("Video", type=["mp4", "mov"])
    if v_file:
        st.video(v_file)
        st.write("Size:", round(v_file.size / 1024 / 1024, 2), "MB")

elif current_id == "m7":
    st.header(choice)
    note = st.text_area("Notes...", height=150)
    if note:
        st.download_button("Save TXT", note, "note.txt")

elif current_id == "m9":
    st.header(choice)
    birthday = st.date_input("Birthday", value=datetime.date(2000, 1, 1))
    def get_zodiac(m, d):
        z = [(1,20,"♑"),(2,19,"♒"),(3,20,"♓"),(4,20,"♈"),(5,21,"♉"),(6,21,"♊"),(7,23,"♋"),(8,23,"♌"),(9,23,"♍"),(10,23,"♎"),(11,22,"♏"),(12,22,"♐"),(12,31,"♑")]
        for month, day, icon in z:
            if m == month and d <= day: return icon
            if m == month - 1: return icon
        return "✨"
    st.success(f"### Result: {get_zodiac(birthday.month, birthday.day)}")

# --- 5. 底部 ---
st.divider()
st.code("geng-tools.streamlit.app", language="text")
