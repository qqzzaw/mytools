import streamlit as st
import requests
from bs4 import BeautifulSoup
import random
import time

# --- 1. 页面配置：更名“模拟系统” ---
st.set_page_config(page_title="模拟系统 / Simulation System", layout="wide")

# 初始化进化记忆 (DNA)
if 'evolution_dna' not in st.session_state:
    st.session_state.evolution_dna = {"keywords": ["秩序", "因果", "转折"], "data_points": 0}
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 2. 自主抓取引擎：定向深度采集 ---
def fetch_online_intelligence(topic):
    """
    自主去网络采集实时数据碎片，作为模拟支撑
    """
    try:
        # 定向从搜索建议和公共文本中获取因果逻辑
        search_url = f"https://bing.com{topic}+可能性"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(search_url, headers=headers, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # 提取真实网页中的逻辑片段
        snippets = [s.get_text() for s in soup.find_all('p') if len(s.get_text()) > 15]
        return snippets
    except:
        return None

# --- 3. 核心模拟引擎：自主逻辑重构 ---
def run_simulation(topic, snippets):
    """
    将抓取到的真实碎片与系统逻辑进行融合进化
    """
    base_logic = [
        "系统判定：该路径具有高度的不确定性。",
        "逻辑演算显示：细微的变量将引发连锁反应。",
        "模拟结果：在该平行维度，你采取了非线性决策。"
    ]
    
    # 提取网络实时碎片
    web_intel = ""
    if snippets:
        st.session_state.evolution_dna["data_points"] += len(snippets)
        intel = random.choice(snippets)[:60]
        web_intel = f"【实时变量注入：{intel}...】"

    # 模拟生成的三个阶段：起因、扰动、状态
    story = f"{random.choice(base_logic)} {web_intel} 最终，系统的预测指向了‘{random.choice(st.session_state.evolution_dna['keywords'])}’的状态。"
    return story

# --- 4. 侧边栏：系统运行参数 ---
with st.sidebar:
    st.title("📟 模拟系统状态")
    st.divider()
    st.metric("已捕获逻辑碎片", st.session_state.evolution_dna["data_points"])
    st.write(f"当前核心关键词: `{', '.join(st.session_state.evolution_dna['keywords'])}`")
    
    st.divider()
    if st.button("重置系统内核"):
        st.session_state.evolution_dna = {"keywords": ["秩序", "因果", "转折"], "data_points": 0}
        st.session_state.history = []
        st.rerun()

# --- 5. 主交互界面 ---
st.markdown("<h1 style='text-align: center;'>🌐 模 拟 系 统</h1>", unsafe_allow_stdio=True)
st.markdown("<p style='text-align: center; color: #888;'>基于网络自主抓取与逻辑进化引擎的情境演化平台</p>", unsafe_allow_stdio=True)

st.write("---")
q = st.text_input("请输入需要演化的决策或变量：", placeholder="例如：离开当前城市 / 启动新项目")

if st.button("🏁 启动逻辑模拟", use_container_width=True):
    if q:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("📡 正在扫描全球实时数据碎片...")
        intel_data = fetch_online_intelligence(q)
        progress_bar.progress(30)
        time.sleep(1)
        
        status_text.text("🧠 逻辑引擎正在自主重构模拟路径...")
        result = run_simulation(q, intel_data)
        progress_bar.progress(70)
        time.sleep(1)
        
        status_text.text("✅ 模拟演化完成。")
        progress_bar.progress(100)
        
        # 展示结果卡片
        st.info(f"### 模拟报告：\n\n{result}")
        st.session_state.history.append({"q": q, "r": result})
        
        # 自主优化互动
        st.divider()
        st.write("🤖 **系统进化反馈：该结果是否符合逻辑？**")
        c1, c2 = st.columns(2)
        if c1.button("符合逻辑（增强该链条）"):
            st.session_state.evolution_dna["keywords"].append("平衡")
            st.toast("逻辑链条已强化。")
        if c2.button("偏离逻辑（重置该链条）"):
            if len(st.session_state.evolution_dna["keywords"]) > 1:
                st.session_state.evolution_dna["keywords"].pop()
            st.toast("逻辑偏差已修正。")

# --- 6. 历史模拟记录 ---
if st.session_state.history:
    with st.expander("📁 历史模拟档案"):
        for h in reversed(st.session_state.history):
            st.write(f"**变量:** {h['q']}")
            st.write(f"**演化结果:** {h['r']}")
            st.write("---")

# --- 7. 合规声明 ---
st.divider()
st.caption("⚖️ 声明：本系统所生成内容均为自主逻辑演化之虚构结果，不具备现实预测性。")
