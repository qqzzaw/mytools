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

# --- 2. 全球语言与时区矩阵 (10种核心语言) ---
LANG_DATA = {
    "English 🇺🇸": {"tz": "UTC", "label": "en"},
    "简体中文 🇨🇳": {"tz": "Asia/Shanghai", "label": "zh"},
    "日本語 🇯🇵": {"tz": "Asia/Tokyo", "label": "ja"},
    "Español 🇪🇸": {"tz": "Europe/Madrid", "label": "es"},
    "Français 🇫🇷": {"tz": "Europe/Paris", "label": "fr"},
    "Deutsch 🇩🇪": {"tz": "Europe/Berlin", "label": "de"},
    "한국어 🇰🇷": {"tz": "Asia/Seoul", "label": "ko"},
    "Русский 🇷🇺": {"tz": "Europe/Moscow", "label": "ru"},
    "Português 🇧🇷": {"tz": "America/Sao_Paulo", "label": "pt"},
    "Tiếng Việt 🇻🇳": {"tz": "Asia/Ho_Chi_Minh", "label": "vi"}
}

# 自动感应初始化
if 'lang' not in st.session_state:
    try:
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        headers = _get_websocket_headers()
        lang_h = headers.get("Accept-Language", "en").lower()
        if "ja" in lang_h: st.session_state.lang = "日本語 🇯🇵"
        elif "zh" in lang_h: st.session_state.lang = "简体中文 🇨🇳"
        else: st.session_state.lang = "English 🇺🇸"
    except:
        st.session_state.lang = "English 🇺🇸"

# --- 3. 侧边栏：精装活日历 + 导航 ---
with st.sidebar:
    st.title("🛠️ GengTools™")
    
    # 【核心修复：实时日历卡片】
    try:
        current_cfg = LANG_DATA.get(st.session_state.lang, LANG_DATA["English 🇺🇸"])
        tz_name = current_cfg["tz"]
        local_tz = pytz.timezone(tz_name)
        now = datetime.datetime.now(local_tz)
        
        # 星期适配逻辑
        week_names = {
            "zh": "星期" + ["一","二","三","四","五","六","日"][now.weekday()],
            "ja": ["月","火","水","木","金","土","日"][now.weekday()] + "曜日",
            "en": now.strftime('%A')
        }
        # 如果不是中日文，默认显示英文星期
        cur_label = current_cfg["label"]
        week_display = week_names.get(cur_label, now.strftime('%A'))
        
        # 渲染黑金卡片 (修复了 unsafe_allow_html 笔误)
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e1e2f 0%, #0e1117 100%); 
                        padding: 15px; border-radius: 12px; border: 1px solid #d4af37; text-align: center; margin-bottom: 10px;">
                <p style="color: #d4af37; margin: 0; font-weight: bold; font-size: 0.9rem;">{week_display}</p>
                <h1 style="margin: 5px 0; color: white; font-size: 2.3rem;">{now.strftime('%H:%M')}</h1>
                <p style="margin: 0; color: #fff;">{now.strftime('%m月%d日') if cur_label != 'en' else now.strftime('%b %d')}</p>
                <p style="margin: 5px 0 0 0; color: #555; font-size: 0.7rem;">{tz_name}</p>
            </div>
        """, unsafe_allow_html=True)
    except:
        st.caption("Time Syncing...")

    st.divider()
    # 语言选择器
    st.session_state.lang = st.selectbox("Language / 语言", list(LANG_DATA.keys()), 
                                         index=list(LANG_DATA.keys()).index(st.session_state.lang))
    
    # 动态工具列表读取
    try:
        df_menu = pd.read_csv("tools_list.csv")
        df_menu.columns = df_menu.columns.str.strip()
        df_menu['id'] = df_menu['id'].astype(str).str.strip().str.lower()
        
        # 智能匹配 CSV 列名
        if "简体中文" in st.session_state.lang: l_col = "name_zh"
        elif "日本語" in st.session_state.lang: l_col = "name_ja"
        else: l_col = "name_en"
        
        options = [f"{row['icon']} {row[l_col]}" for _, row in df_menu.iterrows() if row['id'] != 'm8']
        choice = st.radio("Global Menu", options)
        current_id = str(df_menu.iloc[options.index(choice)]['id']).lower()
    except:
        current_id = "m1"; st.error("Menu Sync Error")

    st.divider()
    st.link_button("🚀 Support via PayPal", "https://paypal.me", use_container_width=True)
    try: st.image("pp_pay.png", use_container_width=True)
    except: pass

# --- 4. 功能逻辑分发 (完整保留所有工具) ---

if current_id == "m1":
    st.header(choice)
    t = st.text_input("Content", "https://")
    if t:
        q_img = qrcode.make(t); b = io.BytesIO(); q_img.save(b, format="PNG")
        st.image(b.getvalue(), width=250); st.download_button("Download", b.getvalue(), "qr.png")

elif current_id == "m2":
    st.header(choice)
    f = st.file_uploader("Image", type=["jpg", "png", "jpeg"])
    if f:
        img = Image.open(f).convert("RGB"); img = ImageOps.exif_transpose(img)
        w, h = img.size; s = min(w, h); img = img.crop(((w-s)//2, (h-s)//2, (w+s)//2, (h+s)//2))
        if st.button("Execute"):
            step = s // 3; cols = st.columns(3)
            for i in range(3):
                for j in range(3):
                    box = (j*step, i*step, (j+1)*step, (i+1)*step)
                    part = img.crop(box); buf = io.BytesIO(); part.save(buf, format="JPEG")
                    cols[j].image(part, use_container_width=True); cols[j].download_button(f"#{i*3+j+1}", buf.getvalue(), f"p_{i*3+j+1}.jpg")

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
    p = st.selectbox("Pair", list(pairs.keys()))
    if st.button("Get Rate"):
        with st.spinner("Syncing..."):
            try:
                tk = yf.Ticker(pairs[p]); r = tk.history(period="1d")['Close'].iloc[-1]
                st.metric("Live Rate", round(r, 4)); st.success(f"Total: {round(amount * r, 2)}")
            except: st.error("Market Busy")

elif current_id == "m5":
    st.header(choice)
    f = st.file_uploader("Image", type=["jpg", "png"])
    if f:
        img = Image.open(f).convert("RGB"); st.image(img, caption="Original")
        if st.button("AI Fix"):
            img = ImageEnhance.Sharpness(img).enhance(2.0); st.image(img, caption="Enhanced")
            buf = io.BytesIO(); img.save(buf, format="JPEG"); st.download_button("Download", buf.getvalue(), "fix.jpg")

elif current_id == "m6":
    st.header(choice)
    vf = st.file_uploader("Video", type=["mp4", "mov"])
    if vf: st.video(vf); st.write("Size:", round(vf.size / 1024 / 1024, 2), "MB")

elif current_id == "m7":
    st.header(choice)
    note = st.text_area("Notes...", height=150)
    if note: st.download_button("Save TXT", note, "note.txt")

elif current_id == "m9":
    st.header(choice)
    bday = st.date_input("Birthday", value=datetime.date(2000, 1, 1))
    def get_z(m, d):
        z = [(1,20,"♑"),(2,19,"♒"),(3,20,"♓"),(4,20,"♈"),(5,21,"♉"),(6,21,"♊"),(7,23,"♋"),(8,23,"♌"),(9,23,"♍"),(10,23,"♎"),(11,22,"♏"),(12,22,"♐"),(12,31,"♑")]
        for month, day, icon in z:
            if m == month and d <= day: return icon
            if m == month - 1: return icon
        return "✨"
    st.success(f"### Result: {get_z(bday.month, bday.day)}")

# --- 5. 底部 ---
st.divider()
st.code("geng-tools.streamlit.app", language="text")
st.caption(f"© {datetime.date.today().year} GengTools™ | Global Active Node")
