import streamlit as st
import random
import time

# --- 1. 自动感应逻辑 ---
try:
    from streamlit.web.server.websocket_headers import _get_websocket_headers
    headers = _get_websocket_headers()
    lang_header = headers.get("Accept-Language", "zh")
    detected_lang = "日本語" if "ja" in lang_header.lower() else "中文"
except:
    detected_lang = "中文"

# --- 2. 翻译字典 ---
LANG_DATA = {
    "中文": {
        "title": "模 拟 系 统",
        "sub": "基于网络自主抓取与逻辑进化引擎的情境演化平台",
        "input_label": "请输入需要演化的变量：",
        "btn": "启动逻辑模拟",
        "status_1": "正在检索逻辑碎片...",
        "status_2": "自律逻辑重构中...",
        "report": "模拟报告",
        "history": "历史模拟档案",
        "local_logic": "系统检测到因果律波动。",
        "placeholder": "例如：去日本发展",
        "detect_msg": "系统已自动匹配语言：简体中文"
    },
    "日本語": {
        "title": "シミュレーション・システム",
        "sub": "自律ロジック進化エンジンによる状況進化プラットフォーム",
        "input_label": "進化させる変数を输入してください：",
        "btn": "ロジックシミュレーション開始",
        "status_1": "ロジック断片を検索中...",
        "status_2": "自律ロジック再構築中...",
        "report": "シミュレーション報告",
        "history": "履歴アーカイブ",
        "local_logic": "因果律の変動を検知しました。",
        "placeholder": "例：日本でのキャリアアップ",
        "detect_msg": "日本語に設定されました"
    }
}

L = LANG_DATA[detected_lang]

# --- 3. 页面配置 ---
st.set_page_config(page_title="Simulation System")

if 'history' not in st.session_state: st.session_state.history = []

# --- 4. 侧边栏 ---
with st.sidebar:
    st.title("System Status")
    st.write(L["detect_msg"])
    if st.button("Reset / 重置"):
        st.session_state.history = []
        st.rerun()

# --- 5. 主界面 (修复了这里引起红屏的 HTML 错误) ---
st.title(L["title"])
st.write(L["sub"])
st.write("---")

q = st.text_input(L["input_label"], placeholder=L["placeholder"])

if st.button(L["btn"], use_container_width=True):
    if q:
        bar = st.progress(0)
        status = st.empty()
        
        status.text(L["status_1"])
        bar.progress(40)
        time.sleep(0.5)
        
        status.text(L["status_2"])
        keywords = ["秩序", "転換", "因果", "次元"] if detected_lang == "日本語" else ["秩序", "转折", "因果", "维度"]
        result = f"{L['local_logic']} | Variable: {q} | Result: {random.choice(keywords)}"
        
        bar.progress(100)
        st.info(f"### {L['report']}：\n\n{result}")
        st.session_state.history.append({"q": q, "r": result})
        st.balloons()
    else:
        st.error("Please input something")

# --- 6. 历史记录 ---
if st.session_state.history:
    with st.expander(L["history"]):
        for h in reversed(st.session_state.history):
            st.write(f"**Variable:** {h['q']} | **Result:** {h['r']}")
