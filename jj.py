import streamlit as st
import pandas as pd
from supabase import create_client, Client
import io

# --- 1. 接入云端大脑 (Supabase) ---
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase: Client = init_connection()

# --- 2. 页面配置 ---
st.set_page_config(page_title="通用工具箱 2.0", layout="wide")

# --- 3. 登录/注册逻辑 (3.0 核心) ---
def login_system():
    with st.sidebar:
        st.title("👤 用户中心")
        if "user" not in st.session_state:
            mode = st.radio("请选择", ["登录", "注册"])
            email = st.text_input("邮箱")
            password = st.text_input("密码", type="password")
            if mode == "注册" and st.button("立即加入"):
                res = supabase.auth.sign_up({"email": email, "password": password})
                st.success("验证邮件已发送，请查收！")
            if mode == "登录" and st.button("进入平台"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.user = res.user
                    st.rerun()
                except:
                    st.error("账号或密码错误")
        else:
            st.write(f"欢迎回来, {st.session_state.user.email}")
            if st.button("退出登录"):
                supabase.auth.sign_out()
                del st.session_state.user
                st.rerun()

# --- 4. 首页逻辑 (读取你之前的 CSV 数据库) ---
def main():
    login_system()
    st.title("🚀 发现您的专属生产力")
    
    # 读取表格
    try:
        df = pd.read_csv("tools_list.csv").fillna("")
        tools = df.to_dict(orient='records')
    except:
        tools = []

    # 搜索框
    q = st.text_input("", placeholder="搜索 100+ 工具...", label_visibility="collapsed")
    
    # 渲染卡片
    for i, t in enumerate(tools):
        if not q or q.lower() in str(t).lower():
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.subheader(t.get('name', '工具'))
                    st.write(t.get('desc', ''))
                with c2:
                    if st.button("立即使用", key=f"run_{i}"):
                        st.session_state.active = t.get('name')
    
    # 底部收款码
    st.sidebar.divider()
    st.sidebar.image("wx.png", caption="支持作者")

if __name__ == "__main__":
    main()
