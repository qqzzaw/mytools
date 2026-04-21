import streamlit as st
import pandas as pd
from pypdf import PdfWriter
import io
import time

# --- 1. 平台级基础配置 ---
st.set_page_config(
    page_title="通用工具箱 2.0",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 响应式美化 CSS
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3rem; font-weight: 600; }
    .tool-card {
        padding: 1.5rem; border-radius: 12px; border: 1px solid #e9ecef;
        background: white; margin-bottom: 1rem;
    }
    .tool-card:hover { border-color: #007bff; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_stdio=True)

# --- 2. 动态数据库加载系统 ---
@st.cache_data(ttl=60) # 缓存数据，每60秒更新一次
def load_tools():
    try:
        # 读取你刚在 GitHub 创建的 tools_list.csv
        df = pd.read_csv("tools_list.csv")
        # 确保数据格式干净
        df = df.fillna("")
        return df.to_dict(orient='records')
    except Exception as e:
        # 如果文件还没创建好，显示一个提示
        return [{"name": "待添加工具", "desc": "请确保 tools_list.csv 已创建", "cate": "全部工具", "type": "internal", "hot": 0, "price": "免费"}]

tools_data = load_tools()

# --- 3. 侧边栏系统 ---
with st.sidebar:
    st.title("🧰 通用工具箱")
    st.caption("可持续运营的工具生态 [v2.0]")
    
    if st.button("👤 登录 / 注册 (预留)"):
        st.toast("正在连接认证服务器...", icon="🔒")
    
    st.divider()
    st.header("📂 导航系统")
    # 分类列表：建议与 tools_list.csv 里的分类保持一致
    main_cate = st.selectbox("核心分类", [
        "全部工具", "1. AI 工具", "2. 开发工具", "3. 设计工具", "4. 办公效率", 
        "5. 云服务", "6. 网络安全", "7. 网络工具", "8. 实用工具", 
        "9. 数据分析", "10. 电商工具", "11. 内容创作", "12. 自动化工具", "13. 学习工具"
    ])
    
    st.divider()
    col1, col2 = st.columns(2)
    with col1: st.image("wx.png", caption="打赏支持")
    with col2: st.image("ali.png", caption="请喝咖啡")
    
    lang = st.selectbox("🌐 语言切换", ["简体中文", "English"])
    admin_mode = st.checkbox("🛠️ 管理后台入口")

# --- 4. 搜索与展示逻辑 ---
st.title("🚀 发现您的专属生产力")
search_q = st.text_input("", placeholder="搜索 100+ 实用工具...", label_visibility="collapsed")

# 过滤逻辑
display_tools = tools_data
if main_cate != "全部工具":
    display_tools = [t for t in display_tools if str(t.get("cate", "")) == main_cate]
if search_q:
    display_tools = [t for t in display_tools if search_q.lower() in str(t).lower()]

# --- 5. 渲染工具矩阵 ---
st.write(f"为您匹配到 `{len(display_tools)}` 个工具")

for i, tool in enumerate(display_tools):
    with st.container():
        st.markdown(f"""
        <div class="tool-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0;">{tool.get('name', '未命名')}</h4>
                <span style="color:#ff4b4b; font-weight:bold;">🔥 {tool.get('hot', 0)}</span>
            </div>
            <p style="color:#6c757d; margin:10px 0;">{tool.get('desc', '')}</p>
        </div>
        """, unsafe_allow_stdio=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.button("查看详情", key=f"det-{i}")
        with c2:
            if tool.get("type") == "internal":
                if st.button("▶️ 立即运行", key=f"run-{i}"):
                    st.session_state.active_tool = tool.get("name")
            else:
                st.link_button("🌐 访问官网", str(tool.get("url", "#")))

# --- 6. 内置功能执行区 (仅在点击运行后出现) ---
if "active_tool" in st.session_state:
    st.divider()
    st.subheader(f"🛠️ 正在运行：{st.session_state.active_tool}")
    if st.button("❌ 关闭工具"):
        del st.session_state.active_tool
        st.rerun()

    # 逻辑 1: PDF 合并
    if st.session_state.active_tool == "PDF 快速合并":
        pdfs = st.file_uploader("上传 PDF", type="pdf", accept_multiple_files=True)
        if pdfs and st.button("开始合并"):
            merger = PdfWriter()
            for p in pdfs: merger.append(p)
            out = io.BytesIO()
            merger.write(out)
            st.success("合并成功！")
            st.download_button("📥 下载文件", out.getvalue(), "merged.pdf")

    # 逻辑 2: AI 生成 (预留)
    elif st.session_state.active_tool == "AI 爆款生成器":
        prompt = st.text_input("输入文案主题...")
        if st.button("AI 生成"):
            st.write(f"【AI 生成中】已收到主题：{prompt}。接入接口后即可导出...")

# --- 7. 后台管理 ---
if admin_mode:
    st.divider()
    st.header("📊 平台管理中心")
    if st.button("🔄 强制刷新数据库"):
        st.cache_data.clear()
        st.success("已同步最新的 tools_list.csv 数据！")
