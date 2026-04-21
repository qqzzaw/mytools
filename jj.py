import streamlit as st
import requests
from bs4 import BeautifulSoup
import random
import time

# --- 1. 页面配置 ---
st.set_page_config(page_title="模拟系统 / Simulation System", layout="wide")

# 初始化进化记忆
if 'evolution_dna' not in st.session_state:
    st.session_state.evolution_dna = {"keywords": ["秩序", "因果", "转折", "维度"], "data_points": 0}
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 2. 稳健抓取引擎 (增加了错误拦截) ---
def fetch_online_intelligence(topic):
    try:
        search_url = f"https://bing.com{topic}+可能性"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        # 增加超时限制，防止卡死
        resp = requests.get(search_url, headers=headers, timeout=3)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            snippets = [s.get_text() for s in soup.find_all('p') if len(s.get_text()) > 15]
            return snippets
        return None
    except:
        # 如果联网失败，返回空，不让程序报错
        return None

# --- 3. 核心模拟引擎 (逻辑增强) ---
def run_simulation(topic, snippets):
    # 本地高质量逻辑库
    local_logics = [
        f"基于变量 '{topic}'，系统检测到非线性波动的因果律。",
        f"在维度索引 042 中，'{topic}' 引发了深层的逻辑重构。",
        f"系统判定：该路径的熵增速度超过预期，演化出未知形态。"
    ]
    
    # 关键词融合
    kw = random.choice(st.session_state.evolution_dna["keywords"])
    
    # 尝试融合网络碎片
    web_intel = ""
    if snippets and len(snippets) > 0:
        st.session_state.evolution_dna["data_points"] += len(snippets)
        intel = random.choice(snippets)[:50]
        web_intel = f"【实时扰动注入：{intel}...】"
    else:
        web_intel = "【网络链路受限，启动本地深度演化模拟】"

    return f"{random.choice(local_logics)} {web_intel} 最终，模拟结果指向：‘{kw}’。"

# --- 4. 侧边栏 ---
with st.sidebar:
    st.title("📟 系统状态")
    st.metric("已捕获碎片", st.session_state.evolution_dna["data_points"])
    st.write(f"当前核心词: `{', '.join(st.session_state.evolution_dna['keywords'])}`")
    if st.button("重置系统"):
        st.session_state.clear()
        st.rerun()

# --- 5. 主界面 ---
st.markdown("<h1 style='text-align: center;'>🌐 模 拟 系 统</h1>", unsafe_allow_stdio=True)
st.write("---")

q = st.text_input("请输入需要演化的变量：", placeholder="例如：换个行业发展")

if st.button("🏁 启动逻辑模拟", use_container_width=True):
    if q:
        bar = st.progress(0)
        status = st.empty()
        
        status.text("📡 正在检索全球逻辑碎片...")
        data = fetch_online_intelligence(q)
        bar.progress(40)
        time.sleep(0.5)
        
        status.text("🧠 自主逻辑重构中...")
        res = run_simulation(q, data)
        bar.progress(100)
        
        st.info(f"### 模拟报告：\n\n{res}")
        st.session_state.history.append({"q": q, "r": res})
        st.balloons()
    else:
        st.error("请输入变量内容")

# --- 6. 历史记录 ---
if st.session_state.history:
    with st.expander("📁 历史模拟档案"):
        for h in reversed(st.session_state.history):
            st.write(f"**变量:** {h['q']} | **结果:** {h['r']}")

st.divider()
st.caption("⚖️ 声明：本系统生成内容均为自主逻辑演化之虚构结果。")
