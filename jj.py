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

# 移动端适配 & 商业化美化 CSS
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

# --- 2. 侧边栏系统 ---
with st.sidebar:
    st.title("🧰 通用工具箱")
    st.caption("可持续运营的工具生态 [v2.0]")
    
    if st.button("👤 登录 / 注册 (预留)"):
        st.toast("正在连接认证服务器...", icon="🔒")
    
    st.divider()
    st.header("📂 导航系统")
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
    admin_mode = st.checkbox("🛠️ 后台管理入口")

# --- 3. 首页搜索与场景筛选 ---
st.title("🚀 发现您的专属生产力")
search_q = st.text_input("", placeholder="搜索 100+ 实用工具、AI 文案或技术脚本...", label_visibility="collapsed")

tags = st.columns(4)
if tags.button("💰 赚钱工具"): search_q = "赚钱"
if tags.button("🧑‍💻 程序员"): search_q = "开发"
if tags.button("🎓 学习辅助"): search_q = "学习"
if tags.button("📱 日常工具"): search_q = "日常"

st.divider()

# --- 4. 融合型工具数据库 ---
# 重点：这里包含了“内置”和“外链”两种工具
tools_data = [
    {
        "name": "PDF 快速合并", 
        "desc": "本地化处理，无需上传云端，隐私绝对安全。", 
        "cate": "4. 办公效率", 
        "type": "internal", # 标记为内置功能
        "hot": 1250, 
        "price": "免费"
    },
    {
        "name": "AI 爆款生成器", 
        "desc": "接入 GPT 接口，一键生成小红书/短视频脚本。", 
        "cate": "1. AI 工具", 
        "type": "internal", # 标记为内置功能
        "hot": 3400, 
        "price": "部分付费"
    },
    {
        "name": "JSON 格式化", 
        "desc": "开发必备，一键美化压缩 JSON 代码。", 
        "cate": "2. 开发工具", 
        "type": "external", # 标记为外部链接
        "url": "https://json.cn",
        "hot": 890, 
        "price": "免费"
    },
]

# 过滤逻辑
display_tools = tools_data
if main_cate != "全部工具":
    display_tools = [t for t in display_tools if t["cate"] == main_cate]
if search_q:
    display_tools = [t for t in display_tools if search_q.lower() in str(t).lower()]

# --- 5. 渲染工具矩阵 (融合渲染) ---
for tool in display_tools:
    with st.container():
        st.markdown(f"""
        <div class="tool-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0;">{tool['name']}</h4>
                <span style="color:#ff4b4b; font-weight:bold;">🔥 {tool['hot']}</span>
            </div>
            <p style="color:#6c757d; margin:10px 0;">{tool['desc']}</p>
        </div>
        """, unsafe_allow_stdio=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.button("查看详情", key=f"det-{tool['name']}")
            
        with c2:
            # 根据类型判断是跳转还是展开内置功能
            if tool["type"] == "internal":
                if st.button("▶️ 立即运行", key=f"run-{tool['name']}"):
                    st.session_state.active_tool = tool['name']
            else:
                st.link_button("🌐 访问官网", tool["url"])

# --- 6. 内置功能执行区 (仅在点击运行后出现) ---
if "active_tool" in st.session_state:
    st.divider()
    st.subheader(f"🛠️ 正在运行：{st.session_state.active_tool}")
    if st.button("❌ 关闭工具"):
        del st.session_state.active_tool
        st.rerun()

    # 具体内置功能的代码逻辑
    if st.session_state.active_tool == "PDF 快速合并":
        pdfs = st.file_uploader("请上传 PDF 文件", type="pdf", accept_multiple_files=True)
        if pdfs and st.button("开始合并"):
            merger = PdfWriter()
            for p in pdfs: merger.append(p)
            out = io.BytesIO()
            merger.write(out)
            st.success("合并成功！")
            st.download_button("📥 下载文件", out.getvalue(), "merged.pdf")

    elif st.session_state.active_tool == "AI 爆款生成器":
        prompt = st.text_input("输入文案主题...")
        if st.button("AI 生成"):
            st.write(f"【AI 模拟结果】：关于‘{prompt}’的爆款文案已生成...")

# --- 7. 管理后台 ---
if admin_mode:
    st.divider()
    st.header("📊 平台管理中心")
    st.info("管理员模式已开启。此处可进行工具增删改查。")
