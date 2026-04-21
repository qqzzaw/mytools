import streamlit as st
import random
import time

# --- 1. 页面配置 (项目名称与 UI 风格) ---
st.set_page_config(page_title="可能性模拟器 / Scenario Generator", layout="centered")

# --- 2. 初始化历史记录 (功能四：历史记录页) ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'page' not in st.session_state:
    st.session_state.page = "home"

# --- 3. 首页 (功能一：Landing Page) ---
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align: center; margin-top: 50px;'>🧠 可能性模拟器</h1>", unsafe_allow_stdio=True)
    st.markdown("<h3 style='text-align: center;'>👉 “输入一个选择，我们生成3种可能的人生故事”</h3>", unsafe_allow_stdio=True)
    st.markdown("<p style='text-align: center; color: #666;'>体验不同选择带来的虚构可能性</p>", unsafe_allow_stdio=True)
    
    st.write(" ")
    if st.button("开始体验", use_container_width=True):
        st.session_state.page = "input"
        st.rerun()

# --- 4. 输入页面 (功能二：核心交互) ---
elif st.session_state.page == "input":
    st.markdown("### 🟡 探索你的可能性")
    
    # ① 输入框 (必填)
    user_q = st.text_input("你想模拟的选择或问题？", placeholder="例如：要不要换工作？ / 今天要不要去见那个人？")
    
    # ② 风格选择
    style = st.selectbox("选择叙事风格", ["普通版", "平静版", "戏剧化版"])
    
    # ③ 生成数量
    count = st.select_slider("生成数量", options=, value=3)
    
    if st.button("生成可能性", use_container_width=True):
        if not user_q:
            st.error("请输入一个选择或问题。")
        else:
            st.session_state.current_q = user_q
            st.session_state.page = "result"
            st.rerun()
    
    if st.button("查看历史记录", variant="secondary"):
        st.session_state.page = "history"
        st.rerun()

# --- 5. 结果页面 (功能三：核心产品) ---
elif st.session_state.page == "result":
    st.markdown(f"### 🔵 针对问题：**{st.session_state.current_q}**")
    st.write("以下是为您生成的虚构情境：")

    # 模拟 AI 生成逻辑 (符合 3-6 句故事结构：起始 -> 变化 -> 结果)
    story_pool = [
        {"title": "意外的转折", "tag": "意外", "content": "你最终选择了踏出那一步。最初的几周充满了不确定性，甚至让你感到焦虑。直到某个午后，一个偶然的电话为你带来了全新的合作机会。现在，你正站在一个从未想象过的高度审视生活，感到一种从未有过的充实。"},
        {"title": "平静的一天", "tag": "平稳", "content": "你决定维持现状。日子依然像往常一样流逝，早晨的咖啡味道依旧熟悉。虽然偶尔会想起那个未曾做出的选择，但你发现当下的安稳才是你最深处的渴望。这种微小的确定性，让你在每个夜晚都能安然入眠。"},
        {"title": "戏剧化的重逢", "tag": "思考型", "content": "那个选择像一颗投入湖心的石子。你开始在陌生的领域摸索，过程比预想的要艰辛许多。在最想放弃的时候，你遇到了一位老友，对方的话语点醒了你。你开始意识到，选择本身不重要，重要的是你重新找回了斗志。"},
        {"title": "轻微的变化", "tag": "轻松", "content": "你换了一种心态去面对。虽然环境没有改变，但你开始在琐碎中寻找乐趣。你发现，其实答案一直都在你心里，只是你之前太焦虑而忽略了它。现在的你，步伐轻盈，对未来充满了柔和的期待。"}
    ]
    
    selected_stories = random.sample(story_pool, st.session_state.count if 'count' in st.session_state else 3)
    
    # 保存到历史记录 (功能四)
    st.session_state.history.append({"q": st.session_state.current_q, "results": selected_stories})

    for res in selected_stories:
        with st.container(border=True):
            st.markdown(f"#### 🧩 {res['title']}")
            st.write(res['content'])
            st.markdown(f"**🧠 情绪标签：{res['tag']}**")

    # 功能五：分享与返回
    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("⬅️ 返回修改问题"):
            st.session_state.page = "input"
            st.rerun()
    with col_b:
        st.button("🔗 生成分享卡片 (模拟)")
        st.caption("提示：长按屏幕截图即可分享当前情境")

# --- 6. 历史记录页 (功能四) ---
elif st.session_state.page == "history":
    st.header("🟣 历史探索记录")
    if not st.session_state.history:
        st.write("暂无记录。")
    else:
        for idx, item in enumerate(st.session_state.history):
            with st.expander(f"问题：{item['q']}"):
                for r in item['results']:
                    st.write(f"**{r['title']}** - {r['content']}")
                if st.button(f"删除记录 {idx}"):
                    st.session_state.history.pop(idx)
                    st.rerun()
    
    if st.button("⬅️ 返回主页"):
        st.session_state.page = "home"
        st.rerun()

# --- 7. 合规声明 (九、合规必须放底部) ---
st.divider()
st.caption("""
⚖️ **合规声明**
* 本网站内容为AI生成的虚构情境，不构成任何现实预测、建议或保证。
* 仅用于娱乐与思考参考。
* ⚠️ 禁止内容：本站严禁生成包含成功/失败、赚钱/亏损等预测性结论。
""")
