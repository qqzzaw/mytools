import streamlit as st
import random
import time

# --- 1. 页面配置与风格优化 ---
st.set_page_config(page_title="可能性模拟器", layout="centered")

# 自定义 CSS 让卡片更有质感
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 25px; height: 3.5rem; font-size: 1.2rem; }
    .stTextArea textarea { border-radius: 15px; }
    .scenario-card { padding: 20px; border-radius: 15px; border: 1px solid #e0e0e0; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_stdio=True)

# --- 2. 状态管理 ---
if 'started' not in st.session_state:
    st.session_state.started = False

# --- 3. 首页 (Landing Page) ---
if not st.session_state.started:
    st.markdown("<h1 style='text-align: center; margin-top: 50px;'>🧠 可能性模拟器</h1>", unsafe_allow_stdio=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #666;'>输入一个选择，我们生成 3 种可能的人生故事</p>", unsafe_allow_stdio=True)
    st.markdown("<p style='text-align: center; color: #888;'>体验不同选择带来的虚构可能性</p>", unsafe_allow_stdio=True)
    
    st.write(" ") 
    if st.button("开始体验"):
        st.session_state.started = True
        st.rerun()
else:
    # --- 4. 核心交互页面 ---
    st.markdown("### 🔍 探索你的平行时空")
    user_input = st.text_area("你正在面临什么选择？", placeholder="例如：要不要离开现在的城市去远方？", height=100)
    
    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox("叙事风格", ["普通版", "平静版", "戏剧化版"])
    with col2:
        count = st.select_slider("生成情境数量", options=[3, 5], value=3)
    
    if st.button("🚀 生成可能性"):
        if not user_input:
            st.warning("请写下你的困惑或选择。")
        else:
            with st.spinner("正在穿越时空，构思虚构的故事..."):
                time.sleep(2)
                
                st.divider()
                st.markdown(f"#### 🎭 针对 '{user_input}' 的模拟结果")
                
                # 故事库（示例，之后可换成AI接口）
                scenarios = [
                    {"title": "意外的转折", "tag": "意外", "content": "你最终选择了出发。在陌生的街道，你因为错过班车而在咖啡馆停留，意外结识了一位正在筹备艺术展的策展人。那天下午的对话，让你重新拿起了画笔。"},
                    {"title": "平静的一天", "tag": "平稳", "content": "生活在细碎中继续。你发现换个环境并不能解决所有烦恼，但空气中湿润的草木香让你在失眠的深夜得到了一丝慰藉。你学会了在阳台种花，心情变得平和。"},
                    {"title": "轻微的变化", "tag": "轻松", "content": "你买了一辆二手单车，开始探索这座城市的巷弄。你不再执着于目标，而是享受风吹过耳边的声音。那个决定没有让你致富，但让你找回了久违的胃口。"},
                    {"title": "思考型转变", "tag": "思考型", "content": "这个决定像一颗石子投入湖心。波纹散去后，你开始意识到真正想改变的不是地址，而是你看待压力的方式。你在静坐中发现，内心的自由是不需要远行的。"},
                    {"title": "时间的礼物", "tag": "温情", "content": "一年后，你偶然翻看旧照片。那个曾经让你纠结万分的决定，如今已成了生命中一段淡然的背景。你感谢当时的勇敢，让你见到了不一样的夕阳。"}
                ]
                
                # 随机抽取
                results = random.sample(scenarios, count)
                
                for res in results:
                    with st.container(border=True):
                        st.subheader(f"🧩 {res['title']}")
                        st.write(res['content'])
                        st.caption(f"📍 情绪标签：{res['tag']} | 虚构情境")
                
                st.balloons()
                if st.button("返回重来"):
                    st.session_state.started = False
                    st.rerun()

# --- 5. 底部合规声明 ---
st.divider()
st.caption("""
**⚖️ 合规声明**
* 本网站内容为AI生成的**虚构情境**，不构成任何现实预测、建议或保证。
* 仅用于娱乐与思考参考。
""")
