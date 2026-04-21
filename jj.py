import streamlit as st
import random
import time

# --- 1. 页面配置 ---
st.set_page_config(page_title="可能性模拟器 / Scenario Generator", layout="centered")

# --- 2. 状态管理 ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'page' not in st.session_state:
    st.session_state.page = "home"

# --- 3. 首页 ---
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align: center; margin-top: 50px;'>🧠 可能性模拟器</h1>", unsafe_allow_stdio=True)
    st.markdown("<h3 style='text-align: center;'>👉 “输入一个选择，我们生成3种可能的人生故事”</h3>", unsafe_allow_stdio=True)
    st.markdown("<p style='text-align: center; color: #666;'>体验不同选择带来的虚构可能性</p>", unsafe_allow_stdio=True)
    
    st.write(" ")
    if st.button("开始体验", use_container_width=True):
        st.session_state.page = "input"
        st.rerun()

# --- 4. 输入页面 ---
elif st.session_state.page == "input":
    st.markdown("### 🟡 探索你的可能性")
    
    user_q = st.text_input("你想模拟的选择或问题？", placeholder="例如：要不要换工作？")
    style = st.selectbox("选择叙事风格", ["普通版", "平静版", "戏剧化版"])
    
    # 【修复重点】这里的 options 括号必须补齐，且加上了具体的数值
    count = st.select_slider("生成数量", options=[3, 5], value=3)
    
    if st.button("生成可能性", use_container_width=True):
        if not user_q:
            st.error("请输入内容。")
        else:
            st.session_state.current_q = user_q
            st.session_state.selected_count = count # 保存选择的数量
            st.session_state.page = "result"
            st.rerun()
    
    if st.button("查看历史记录"):
        st.session_state.page = "history"
        st.rerun()

# --- 5. 结果页面 ---
elif st.session_state.page == "result":
    st.markdown(f"### 🔵 针对问题：**{st.session_state.current_q}**")
    
    # 模拟故事库
    story_pool = [
        {"title": "意外的转折", "tag": "意外", "content": "你选择了踏出那一步。最初充满了不确定性，直到一个偶然的电话为你带来了全新的机会。"},
        {"title": "平静的一天", "tag": "平稳", "content": "你决定维持现状。日子依旧熟悉，你发现当下的安稳才是你最深处的渴望。"},
        {"title": "戏剧化的重逢", "tag": "思考型", "content": "选择像石子投入湖心。在最想放弃时遇到老友，你意识到斗志比选择更重要。"},
        {"title": "轻微的变化", "tag": "轻松", "content": "换种心态面对，环境没变但你开始寻找琐碎的乐趣，步伐变得轻盈。"},
        {"title": "时间的礼物", "tag": "思考型", "content": "一年后翻看旧照，当初纠结的选择已成淡然背景，你感谢那份勇敢。"}
    ]
    
    # 根据用户选择的数量随机抽取
    num = st.session_state.selected_count
    selected_stories = random.sample(story_pool, min(num, len(story_pool)))
    
    # 保存历史
    st.session_state.history.append({"q": st.session_state.current_q, "results": selected_stories})

    for res in selected_stories:
        with st.container(border=True):
            st.markdown(f"#### 🧩 {res['title']}")
            st.write(res['content'])
            st.markdown(f"**🧠 情绪标签：{res['tag']}**")

    if st.button("⬅️ 返回修改问题"):
        st.session_state.page = "input"
        st.rerun()

# --- 6. 历史记录页 ---
elif st.session_state.page == "history":
    st.header("🟣 历史记录")
    if not st.session_state.history:
        st.write("暂无记录。")
    else:
        for idx, item in enumerate(st.session_state.history):
            with st.expander(f"问题：{item['q']}"):
                for r in item['results']:
                    st.write(f"**{r['title']}** - {r['content']}")
    
    if st.button("⬅️ 返回主页"):
        st.session_state.page = "home"
        st.rerun()

# --- 7. 合规声明 ---
st.divider()
st.caption("⚖️ 合规声明：本站内容为AI生成的虚构情境，仅用于娱乐与思考参考。")
