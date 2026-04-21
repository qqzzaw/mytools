import streamlit as st
import pandas as pd
from PIL import Image
import io

# --- 1. 平台级配置 ---
st.set_page_config(
    page_title="通用工具箱 - 专业级工具生态平台",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 移动端 & 平台美化 CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5rem; }
    .tool-card {
        padding: 20px; border-radius: 12px; border: 1px solid #eee;
        background: white; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    /* 适配手机端标题 */
    @media (max-width: 640px) { .header-text { font-size: 1.5rem !important; } }
    </style>
    """, unsafe_allow_stdio=True)

# --- 2. 侧边栏：用户系统与多语言 ---
with st.sidebar:
    st.title("🧰 通用工具箱 2.0")
    
    # 【用户系统入口】
    if st.button("👤 登录 / 注册"):
        st.toast("用户系统模块加载中...", icon="👤")
    
    st.divider()
    # 【多语言切换】
    lang = st.selectbox("🌐 语言 / Language", ["简体中文", "English", "日本語"])
    
    # 【多级分类导航】
    st.header("📂 工具分类")
    main_cate = st.radio("主分类", [
        "全部工具", "AI 智能", "开发工具", "设计工具", "办公效率", 
        "云服务", "网络安全", "内容创作", "学习工具"
    ])
    
    st.divider()
    st.write("☕ **赞助与支持**")
    c1, c2 = st.columns(2)
    with c1: st.image("wx.png", use_container_width=True)
    with c2: st.image("ali.png", use_container_width=True)

# --- 3. 首页系统：搜索与推荐 ---
st.markdown("<h1 class='header-text'>🚀 发现更高效的工具生态</h1>", unsafe_allow_stdio=True)

# 【全站搜索系统】
search_col, filter_col = st.columns([4, 1])
with search_col:
    q = st.text_input("", placeholder="搜索 100+ 实用工具、AI 模型或技术文档...", label_visibility="collapsed")
with filter_col:
    st.button("🔍 搜索")

# 【用途入口 - 快速筛选】
st.write("### 🎯 快速入口")
tags = st.columns(4)
tags[0].button("💰 赚钱工具")
tags[1].button("🧑‍💻 开发者")
tags[2].button("🎓 学习辅助")
tags[3].button("📱 日常生活")

st.divider()

# --- 4. 工具展示系统 (结构化内容) ---
# 模拟一个结构化的工具列表
tools = [
    {
        "id": "pdf-merge",
        "name": "PDF 快速合并",
        "desc": "本地化处理，保护文档安全。支持批量操作。",
        "cate": "办公效率",
        "tag": "免费 / Web / 无需注册",
        "hot": 999
    },
    {
        "id": "ai-write",
        "name": "AI 爆款文案生成",
        "desc": "接入最新大模型，一键生成小红书、短视频脚本。",
        "cate": "AI 智能",
        "tag": "部分付费 / AI / 创作",
        "hot": 1500
    }
]

st.write("### 🔥 热门推荐")
for tool in tools:
    with st.container():
        # 结构化展示，适配手机
        st.markdown(f"""
        <div class="tool-card">
            <h4>{tool['name']} <span style="font-size:12px; color:#ff4b4b;">🔥 {tool['hot']}</span></h4>
            <p style="color:#666; font-size:14px;">{tool['desc']}</p>
            <p style="font-size:12px; color:#999;">标签: {tool['tag']}</p>
        </div>
        """, unsafe_allow_stdio=True)
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            if st.button("详情", key=tool['id']):
                st.session_state.current_tool = tool['id']
        with col_btn2:
            st.button("立即使用", key=f"run-{tool['id']}")

# --- 5. 后台管理系统预留 (隐藏入口) ---
if st.sidebar.checkbox("🛠️ 后台管理 (仅管理员)", value=False):
    st.divider()
    st.header("📊 平台管理中心")
    tab1, tab2, tab3 = st.tabs(["工具管理", "用户统计", "SEO设置"])
    with tab1:
        st.button("➕ 新增工具")
        st.write("当前工具列表：PDF合并, AI文案...")
    with tab2:
        st.line_chart(pd.DataFrame([10, 20, 15, 30], columns=["访问量"]))
