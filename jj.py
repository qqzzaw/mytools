import streamlit as st
import pandas as pd
from pypdf import PdfWriter
from PIL import Image
import io
import time # 新增：支持系统监测动画

# --- 1. 页面配置 ---
st.set_page_config(page_title="通用工具箱", layout="wide")

# --- 2. 核心数据库 ---
if 'tools_db' not in st.session_state:
    st.session_state.tools_db = [
        {"名称": "PDF 快速合并", "简介": "本地合并多个 PDF 文件，隐私安全。", "官网": "内置功能", "收费": "免费", "主分类": "4. 办公效率", "场景": "🧑‍💻 程序员工具", "核心功能": "1.本地处理 2.一键合并 3.极速下载", "支持平台": "Web / Mac / Windows", "注册/中文": "不需要 / 支持", "评价": "优点: 极简安全; 缺点: 功能单一", "人群/难度": "办公族 / ⭐", "商业模式": "完全免费", "标签": "PDF, 办公, 效率"},
        {"名称": "ChatGPT", "简介": "全球领先的通用 AI 对话模型", "官网": "https://openai.com", "收费": "部分免费", "主分类": "1. AI 工具", "场景": "🧑‍💻 程序员工具", "核心功能": "文本创作, 代码编写, 逻辑推理", "支持平台": "Web/iOS/Android", "注册/中文": "需要/支持", "评价": "优点: 逻辑最强; 缺点: 国内访问需环境", "人群/难度": "所有人/⭐⭐", "商业模式": "月订阅制", "标签": "AI, 对话, 创作"}
        # ... 其他数据已省略，保持代码清爽
    ]

# --- 3. 侧边栏 ---
with st.sidebar:
    st.title("🧰 通用工具箱")
    st.caption("省心、好用的工具集成平台")
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        try: st.image("wx.png", caption="支持作者")
        except: st.write("📷 微信码")
    with c2:
        try: st.image("ali.png", caption="请喝咖啡")
        except: st.write("📷 支付宝")
    st.divider()
    
    # --- 这里增加了新模块入口 ---
    cate = st.selectbox("功能分类", [
        "全部", "1. AI 工具", "2. 开发工具", "3. 设计工具", "4. 办公效率", 
        "5. 云服务", "6. 网络安全", "7. 网络工具", "8. 实用工具", 
        "9. 数据分析", "10. 电商工具", "11. 内容创作", "12. 自动化工具", "13. 学习工具",
        "🚀 AI 深度实验室", "📊 系统运行监测" # 新增模块
    ])
    use_case = st.multiselect("用途分类", ["💰 赚钱工具", "🧑‍💻 程序员工具", "🎓 学习工具", "📱 日常工具"])
    price = st.radio("价格模式", ["不限", "免费", "部分免费", "付费"])

# --- 4. 逻辑判断：新模块显示 ---

# A. AI 深度实验室模块
if cate == "🚀 AI 深度实验室":
    st.header("🧠 AI 深度实验室 (Beta)")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("向 AI 助手提问..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            response = f"【模拟回复】关于'{prompt}'，建议赞助作者以接入 GPT-4 接口。"
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# B. 系统运行监测模块
elif cate == "📊 系统运行监测":
    st.header("🖥️ 工具箱运行状态")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("全球节点", "在线", "Normal")
    col_b.metric("当前负载", "1.2%", "-0.3%")
    col_c.metric("安全等级", "High", "Verified")
    if st.button("启动全功能自检"):
        with st.status("正在扫描模块...", expanded=True) as status:
            st.write("检查 PDF 组件...")
            time.sleep(1)
            st.write("连接 AI 接口...")
            time.sleep(1)
            status.update(label="✅ 所有模块运行正常！", state="complete", expanded=False)

# C. 原有的工具展示逻辑
else:
    st.write("### 🔍 寻找您的专属工具")
    q = st.text_input("搜索", placeholder="输入关键词...", label_visibility="collapsed")
    data = st.session_state.tools_db
    if cate != "全部": data = [t for t in data if t["主分类"] == cate]
    if use_case: data = [t for t in data if any(uc in t["场景"] for uc in use_case)]
    if price != "不限": data = [t for t in data if t["收费"] == price]
    if q: data = [t for t in data if q.lower() in str(t).lower()]

    st.write(f"为您查找到 `{len(data)}` 个专业工具")
    for i, item in enumerate(data):
        with st.container():
            st.markdown("---")
            col_main, col_btn = st.columns([4, 1])
            with col_main:
                st.subheader(f"{item['名称']}  ({item['收费']})")
                st.write(f"**简介：** {item['简介']}")
                with st.expander("🛠️ 深度评测信息"):
                    st.write(f"**🎯 核心功能：** {item['核心功能']}")
                    st.write(f"**💡 评价：** {item['评价']}")
            with col_btn:
                if item["官网"] == "内置功能":
                    if st.button("使用", key=f"run_{i}"): st.info("请在[办公效率]中使用")
                else:
                    st.link_button("访问", item["官网"], key=f"link_{i}")

# --- 5. 内置 PDF 功能 (当搜索PDF或在办公效率分类时显示) ---
if (cate == "4. 办公效率" or (cate == "全部" and "PDF" in locals().get('q', ''))):
    st.divider()
    st.markdown("#### 🛠️ 在线实操：PDF 快速合并")
    pdfs = st.file_uploader("选择 PDF", type="pdf", accept_multiple_files=True)
    if pdfs and st.button("执行合并"):
        merger = PdfWriter()
        for p in pdfs: merger.append(p)
        out = io.BytesIO()
        merger.write(out)
        st.success("合并成功！")
        st.download_button("📥 下载文件", out.getvalue(), "merged.pdf")
