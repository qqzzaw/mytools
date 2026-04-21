import streamlit as st
import random
import time

# --- 1. 基础配置 ---
st.set_page_config(page_title="可能性模拟器", layout="centered")

# 初始化状态
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 2. 首页模块 ---
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align: center;'>🧠 可能性模拟器</h1>", unsafe_allow_stdio=True)
    st.markdown("<h3 style='text-align: center;'>👉 输入一个选择，生成3种虚构人生故事</h3>", unsafe_allow_stdio=True)
    st.write(" ")
    if st.button("开始体验", use_container_width=True):
        st.session_state.page = "input"
        st.rerun()

# --- 3. 输入模块 ---
elif st.session_state.page == "input":
    st.header("🟡 探索你的可能性")
    user_q = st.text_input("你想模拟的选择或问题？", placeholder="例如：要不要去新的城市？")
    
    style = st.selectbox("选择叙事风格", ["普通版", "平静版", "戏剧化版"])
    # 简化选择方式，防止报错
    count = st.radio("生成情境数量", [3, 5], index=0)
    
    if st.button("🚀 生成可能性", use_container_width=True):
        if user_q:
            st.session_state.current_q = user_q
            st.session_state.selected_count = count
            st.session_state.page = "result"
            st.rerun()
        else:
            st.error("请先输入内容")

# --- 4. 结果模块 ---
elif st.session_state.page == "result":
    st.header(f"🔵 模拟结果：{st.session_state.current_q}")
    
    # 预设故事池
    pool = [
        {"t": "意外的转折", "tag": "意外", "c": "你踏出了那一步。最初几周充满焦虑，直到一个偶然的电话为你带来了全新的机会，那是你从未想象过的高度。"},
        {"t": "平静的一天", "tag": "平稳", "c": "你决定维持现状。日子依旧熟悉，咖啡味道未变。你发现当下的安稳才是你最深处的渴望，这种确定性让你安稳。"},
        {"t": "思考型转变", "tag": "思考", "c": "选择像石子投入湖心。在最想放弃时遇到老友，你意识到选择本身不重要，重要的是你重新找回了斗志。"},
        {"t": "轻微的变化", "tag": "轻松", "c": "换种心态面对，环境没变但你开始寻找琐碎的乐趣。步伐变得轻盈，对未来充满了柔和的期待。"},
        {"t": "时间的礼物", "tag": "意外", "c": "一年后翻看旧照，当初纠结的选择已成淡然背景。你感谢那份勇敢，让你见到了不一样的夕阳。"}
    ]
    
    selected = random.sample(pool, min(st.session_state.selected_count, len(pool)))
    
    for item in selected:
        with st.container(border=True):
            st.subheader(f"🧩 {item['t']}")
            st.write(item['c'])
            st.caption(f"🧠 情绪标签：{item['tag']}")
    
    if st.button("⬅️ 返回修改"):
        st.session_state.page = "input"
        st.rerun()

# --- 5. 底部合规 ---
st.divider()
st.caption("⚖️ 合规声明：本站内容为虚构故事，不构成现实建议，仅供娱乐。")
