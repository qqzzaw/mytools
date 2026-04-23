import streamlit as st
import pandas as pd
from PIL import Image, ImageOps, ImageEnhance
import yfinance as yf
import qrcode
import io
import datetime
import time
import pytz

st.set_page_config(page_title="GengTools™", page_icon="🛠️", layout="centered")

@st.cache_data(ttl=60)
def load_config():
    try:
        df = pd.read_csv("tools_list.csv")
        df.columns = df.columns.str.strip()
        df['id'] = df['id'].astype(str).str.strip().str.lower()
        return df
    except:
        return pd.DataFrame([{"id":"m1","name_en":"QR","name_zh":"二维码","name_ja":"QR","icon":"📱"}])

df_menu = load_config()

with st.sidebar:
    st.title("🛠️ GengTools™")
    lang = st.selectbox("Language", ["English", "简体中文", "日本語"])
    lang_map = {"English": "name_en", "简体中文": "name_zh", "日本語": "name_ja"}
    
    st.divider()
    options = [f"{row['icon']} {row[lang_map[lang]]}" for _, row in df_menu.iterrows()]
    choice = st.radio("Menu", options)
    current_id = str(df_menu.iloc[options.index(choice)]['id']).lower()

    st.divider()
    st.link_button("🚀 PayPal", "https://paypal.me", use_container_width=True)
    st.caption(f"🟢 System: Online")

if current_id == "m8":
    st.header(choice)
    tz_dict = {
        "China (Beijing)": "Asia/Shanghai",
        "Japan (Tokyo)": "Asia/Tokyo",
        "USA (New York)": "America/New_York",
        "UK (London)": "Europe/London",
        "Germany (Berlin)": "Europe/Berlin"
    }
    
    col1, col2 = st.columns(2)
    with col1:
        sel_tz = st.selectbox("Select Region / 选择地区", list(tz_dict.keys()))
    
    target_tz = pytz.timezone(tz_dict[sel_tz])
    now_time = datetime.datetime.now(target_tz)
    
    with col2:
        st.metric("Local Time", now_time.strftime('%H:%M:%S'))
    
    st.write(f"📅 **Date:** {now_time.strftime('%Y-%m-%d')}")
    st.info(f"Current timezone: {tz_dict[sel_tz]}")

elif current_id == "m9":
    st.header(choice)
    birthday = st.date_input("Select Birthday / 选择生日", value=datetime.date(2000, 1, 1))
    
    def get_zodiac(month, day):
        zodiacs = [
            (1, 20, "Capricorn ♑", "摩羯座", "山羊座"), (2, 19, "Aquarius ♒", "水瓶座", "水瓶座"),
            (3, 20, "Pisces ♓", "双鱼座", "魚座"), (4, 20, "Aries ♈", "白羊座", "牡羊座"),
            (5, 21, "Taurus ♉", "金牛座", "牡牛座"), (6, 21, "Gemini ♊", "双子座", "双子座"),
            (7, 23, "Cancer ♋", "巨蟹座", "蟹座"), (8, 23, "Leo ♌", "狮子座", "獅子座"),
            (9, 23, "Virgo ♍", "处女座", "乙女座"), (10, 23, "Libra ♎", "天秤座", "天秤座"),
            (11, 22, "Scorpio ♏", "天蝎座", "蠍座"), (12, 22, "Sagittarius ♐", "射手座", "射手座"),
            (12, 31, "Capricorn ♑", "摩羯座", "山羊座")
        ]
        for m, d, en, zh, ja in zodiacs:
            if (month == m and day <= d) or (month == m - 1):
                return {"English": en, "简体中文": zh, "日本語": ja}
        return {"English": "Capricorn ♑", "简体中文": "摩羯座", "日本語": "山羊座"}

    res = get_zodiac(birthday.month, birthday.day)
    st.success(f"### {res[lang]}")
    st.write("✨ **Today's Tip:** Focus on your goals and stay creative!")

elif current_id == "m1":
    st.header(choice)
    text = st.text_input("Content")
    if text and qrcode:
        qr_img = qrcode.make(text)
        buf = io.BytesIO(); qr_img.save(buf, format="PNG")
        st.image(buf.getvalue(), width=250)

st.write("---")
st.success("📸 **TikTok Lite / SNS Poster**")
st.code("geng-tools.streamlit.app", language="text")
