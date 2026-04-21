import streamlit as st
import pandas as pd
from pypdf import PdfWriter
from PIL import Image, ImageOps
import io
import random
import string
import requests

# --- 1. 页面配置与美化 ---
st.set_page_config(page_title="Geng-Tools 全能工具矩阵", layout="wide")

st.markdown("""
    <style>
    .stSelectbox div[data-baseweb="select"] { background-color: #f0f2f6; border-radius: 10px; }
    .st-emotion-cache-1avm0fb { padding: 1rem; border-radius: 15px; border: 1px solid #e6e9ef; }
    </style>
    """, unsafe_allow_stdio=True)

# --- 2. 侧边栏：收银台与大分类导航 ---
with st.sidebar:
    st.title("🛡️ Geng-Tools 矩阵")
    st.write("---")
    # 双码收银台
    col1, col2 = st.columns(2)
    with col1:
        try: st.image("wx.png", caption="微信赞赏")
        except: st.caption("📸 缺失wx.png")
    with col2:
        try: st.image("ali.png", caption="支付宝赞助")
        except: st.caption("📸 缺失ali.png")
    
    st.divider()
    # 按照你的要求排序的 13 大分类
    main_menu = st.selectbox("📂 选择一级分类", [
        "1. AI 智能工具", "2. 开发辅助工具", "3. 专业设计工具", 
        "4. 办公效率神器", "5. 云服务/网络安全", "6. 实用生活工具", 
        "7. 数据分析专区", "8. 电商运营工具", "9. 内容创作助手", 
        "10. 自动化脚本", "11. 学习辅助工具"
    ])
    st.caption("版本: v5.0 矩阵版 | 开发者: Geng")

# --- 3. 核心功能逻辑 ---

# 分类 1: AI 智能工具
if "1." in main_menu:
    st.header("🤖 AI 智能工具箱")
    t1, t2, t3 = st.tabs(["文本生成", "AI 助手", "创作灵感"])
    with t1:
        prompt = st.text_area("输入需求...", placeholder="例如：帮我写一段电商文案")
        if st.button("🚀 AI 立即生成"):
            st.info(f"AI 正在为您处理：{prompt[:10]}...")
            st.write("【模拟结果】：这是为您定制的专业文案内容，赞助后可接入 GPT-4 接口。")

# 分类 2: 开发辅助工具
elif "2." in main_menu:
    st.header("💻 开发者实验室")
    t1, t2 = st.tabs(["代码格式化", "强密码生成"])
    with t1:
        st.code("def hello_world():\n    print('Hello Geng-Tools!')", language='python')
        st.caption("代码高亮已开启")
    with t2:
        length = st.slider("长度", 8, 32, 16)
        if st.button("🎲 生成密钥"):
            pwd = ''.join(random.choice(string.ascii_letters + string.digits + "!@#$%^&*") for _ in range(length))
            st.code(pwd)

# 分类 3: 专业设计工具
elif "3." in main_menu:
    st.header("🎨 设计与视觉中心")
    img = st.file_uploader("上传图片资源", type=["jpg", "png"])
    if img:
        image = Image.open(img)
        st.image(image, width=300)
        if st.button("🚀 一键转为黑白线稿"):
            st.image(ImageOps.grayscale(image))

# 分类 4: 办公效率神器 (原有 PDF/Excel 整合)
elif "4." in main_menu:
    st.header("🏢 极速办公套件")
    t1, t2 = st.tabs(["PDF 合并", "Excel 对账"])
    with t1:
        pdfs = st.file_uploader("PDF文件", type="pdf", accept_multiple_files=True)
        if pdfs and st.button("合并"):
            merger = PdfWriter()
            for p in pdfs: merger.append(p)
            out = io.BytesIO()
            merger.write(out)
            st.download_button("📥 下载", out.getvalue(), "merged.pdf")

# 分类 5: 云服务/网络安全/网络工具
elif "5." in main_menu:
    st.header("🌐 云与网络安全")
    st.write("### 🛠️ 网络工具箱")
    st.button("🔍 扫描端口 (模拟)")
    st.button("🛡️ 检查网址安全性 (模拟)")
    st.text_input("输入 IP 地址查看归属地")

# 分类 6: 实用生活工具 (原有 BMI/二维码)
elif "6." in main_menu:
    st.header("🛠️ 实用生活助手")
    t1, t2 = st.tabs(["二维码生成", "BMI 计算"])
    with t1:
        url = st.text_input("链接转二维码")
        if url: st.image(f"https://qrserver.com{url}")

# 分类 7: 数据分析专区
elif "7." in main_menu:
    st.header("📊 深度数据分析")
    st.write("上传 CSV/Excel 获取数据报告")
    st.button("📈 生成可视化图表 (预留)")

# 分类 8: 电商运营工具
elif "8." in main_menu:
    st.header("📦 电商运营百宝箱")
    st.selectbox("选择平台", ["淘宝/天猫", "京东", "拼多多", "亚马逊"])
    st.button("📝 一键生成商品标题")
    st.button("💰 利润计算器")

# 分类 9: 内容创作助手
elif "9." in main_menu:
    st.header("✍️ 创作工厂")
    st.text_input("输入关键词获取爆款标题")
    st.button("🎬 视频分镜脚本生成")

# 分类 10: 自动化工具
elif "10." in main_menu:
    st.header("🤖 自动化执行器")
    st.write("编写你的自动化任务...")
    st.code("# 模拟脚本: 自动备份文件\ncopy source_dir backup_dir")

# 分类 11: 学习辅助工具
elif "11." in main_menu:
    st.header("🎓 智慧学习中心")
    st.button("📖 单词背诵助手")
    st.button("⏳ 专注番茄钟")
