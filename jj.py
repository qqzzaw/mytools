import streamlit as st
import pandas as pd
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import yfinance as yf
import qrcode
import io
import datetime
import time
import pytz

# ==========================================
# 【第一部分：主板区】—— 这部分以后永远不改
# ==========================================
st.set_page_config(page_title="GengTools™ Global", page_icon="🛠️", layout="centered")

# 1. 语言与时区矩阵
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

if 'lang' not in st.session_state:
    st.session_state.lang = "English 🇺🇸"

# 2. 侧边栏构建
with st.sidebar:
    st.title("🛠️ GengTools™")
    
    # 实时金边时钟 (核心修复版)
    try:
        cfg = LANG_DATA.get(st.session_state.lang, LANG_DATA["English 🇺🇸"])
        tz = pytz.timezone(cfg["tz"])
        now = datetime.datetime.now(tz)
        week_names = {"zh": "星期" + ["一","二","三","四","五","六","日"][now.weekday()],
                      "ja": ["月","火","水","木","金","土","日"][now.weekday()] + "曜日",
                      "en": now.strftime('%A')}
        week_str = week_names.get(cfg["label"], now.strftime('%A'))
        
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e1e2f 0%, #0e1117 100%); 
                        padding: 15px; border-radius: 12px; border: 1px solid #d4af37; text-align: center; margin-bottom: 10px;">
                <p style="color: #d4af37; margin: 0; font-weight: bold;">{week_str}</p>
                <h1 style="margin: 5px 0; color: white; font-size: 2.2rem;">{now.strftime('%H:%M')}</h1>
                <p style="margin: 0; color: #fff;">{now.strftime('%m月%d日') if cfg['label'] != 'en' else now.strftime('%b %d')}</p>
            </div>
        """, unsafe_allow_html=True)
    except: st.caption("Syncing...")

    st.divider()
    st.session_state.lang = st.selectbox("Language / 语言", list(LANG_DATA.keys()), 
                                         index=list(LANG_DATA.keys()).index(st.session_state.lang))
    
    # 动态读取 CSV 菜单
    try:
        df = pd.read_csv("tools_list.csv")
        df.columns = df.columns.str.strip()
        df['id'] = df['id'].astype(str).str.strip().str.lower()
        l_col = "name_zh" if "简体" in st.session_state.lang else ("name_ja" if "日本語" in st.session_state.lang else "name_en")
        options = [f"{row['icon']} {row[l_col]}" for _, row in df.iterrows() if row['id'] != 'm8']
        choice = st.radio("Menu", options)
        current_id = str(df.iloc[options.index(choice)]['id']).lower()
    except: current_id = "m1"

    st.divider()
    st.link_button("🚀 Support via PayPal", "https://paypal.me", use_container_width=True)
    try: st.image("pp_pay.png", use_container_width=True)
    except: pass

# ==========================================
# 【第二部分：插件分发区】—— 以后加功能只在这里“加分支”
# ==========================================

st.header(choice)

if current_id == "m1": # 二维码
    t = st.text_input("Content", "https://")
    if t:
        img = qrcode.make(t); buf = io.BytesIO(); img.save(buf, format="PNG")
        st.image(buf.getvalue(), width=250); st.download_button("Download", buf.getvalue(), "qr.png")

elif current_id == "m2": # 九宫格
    f = st.file_uploader("Upload", type=["jpg", "png"])
    if f:
        img = Image.open(f).convert("RGB"); img = ImageOps.exif_transpose(img)
        w, h = img.size; s = min(w, h); img = img.crop(((w-s)//2, (h-s)//2, (w+s)//2, (h+s)//2))
        if st.button("Run"):
            step = s // 3; cols = st.columns(3)
            for i in range(3):
                for j in range(3):
                    box = (j*step, i*step, (j+1)*step, (i+1)*step)
                    part = img.crop(box); b = io.BytesIO(); part.save(b, format="JPEG")
                    cols[j].image(part, use_container_width=True); cols[j].download_button(f"#{i*3+j+1}", b.getvalue(), f"p.jpg")

elif current_id == "m4": # 汇率
    amt = st.number_input("Amount", value=100.0)
    pair = st.selectbox("Pair", ["USD/CNY", "USD/JPY", "CNY/JPY"])
    if st.button("Get Rate"):
        try:
            tk = yf.Ticker(pair.replace("/","")+"=X"); r = tk.history(period="1d")['Close'].iloc[-1]
            st.metric("Live Rate", round(r, 4)); st.success(f"Total: {round(amt * r, 2)}")
        except: st.error("Market Busy")

elif current_id == "m3": # TikTok 热门标签
    kw = st.text_input("TikTok Topic / 话题关键词", "Viral")
    if st.button("Generate Tags"):
        tags = [f"#{kw}", "#fyp", "#viral", "#trending", "#foryou", "#useful", "#tools"]
        st.code(" ".join(tags))

elif current_id == "m6": # 视频信息
    vf = st.file_uploader("Upload Video File", type=["mp4", "mov"])
    if vf:
        st.video(vf)
        st.write(f"📁 **File Size:** {round(vf.size / 1024 / 1024, 2)} MB")
        st.info("Analysis: Ready for HD Upload.")

elif current_id == "m7": # 智能笔记
    note = st.text_area("Write your notes here...", height=200)
    if note:
        st.download_button("Save as .txt", note, "my_note.txt")

   elif current_id == "m8": # 把它从 m9 改成 m8，就对上了！
    st.header(choice)
    birthday = st.date_input("Select Birthday / 选择生日", value=datetime.date(2000, 1, 1))
    
    def get_zodiac_sign(m, d):
        signs = [
            (1, 20, "摩羯座 Capricorn ♑"), (2, 19, "水瓶座 Aquarius ♒"),
            (3, 20, "双鱼座 Pisces ♓"), (4, 20, "白羊座 Aries ♈"),
            (5, 21, "金牛座 Taurus ♉"), (6, 21, "双子座 Gemini ♊"),
            (7, 23, "巨蟹座 Cancer ♋"), (8, 23, "狮子座 Leo ♌"),
            (9, 23, "处女座 Virgo ♍"), (10, 23, "天秤座 Libra ♎"),
            (11, 22, "天蝎座 Scorpio ♏"), (12, 22, "射手座 Sagittarius ♐"),
            (12, 31, "摩羯座 Capricorn ♑")
        ]
        for month, day, name in signs:
            if m == month and d <= day: return name
            if m == month - 1: return name
        return "✨"

    result = get_zodiac_sign(birthday.month, birthday.day)
    st.success(f"### {result}")


# ------------------------------------------
# 💡 这里是你的“精装修”区域：以后加东西，就在下面直接写新的 elif
# ------------------------------------------

elif current_id == "m5": # 照片优化
    f = st.file_uploader("Image", type=["jpg", "png"])
    if f:
        img = Image.open(f).convert("RGB")
        if st.button("AI Fix"):
            img = ImageEnhance.Sharpness(img).enhance(2.0)
            st.image(img, caption="Enhanced"); b = io.BytesIO(); img.save(b, format="JPEG")
            st.download_button("Download", b.getvalue(), "fix.jpg")

elif current_id == "m9": # 星座
    bd = st.date_input("Birthday", value=datetime.date(2000, 1, 1))
    def get_z(m, d):
        z = [(1,20,"♑"),(2,19,"♒"),(3,20,"♓"),(4,20,"♈"),(5,21,"♉"),(6,21,"♊"),(7,23,"♋"),(8,23,"♌"),(9,23,"♍"),(10,23,"♎"),(11,22,"♏"),(12,22,"♐"),(12,31,"♑")]
        for month, day, icon in z:
            if m == month and d <= day: return icon
            if m == month - 1: return icon
        return "✨"
    st.success(f"### Result: {get_z(bd.month, bd.day)}")

# --- 底部 ---
st.divider()
st.code("geng-tools.streamlit.app")
