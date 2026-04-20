import streamlit as st
import pandas as pd
from pypdf import PdfWriter
from PIL import Image, ImageOps
import io
import random
import string
import time

# --- 1. 页面配置 ---
st.set_page_config(page_title="Geng-Tools 终极全能王", layout="wide")

# 自定义风格：让侧边栏更醒目
st.markdown("""
    <style>
    .st-emotion-cache-16idsys p { font-size: 1.1rem; font-weight: 500; }
    .stButton button { border-radius: 20px; transition: 0.3s; }
    .stButton button:hover { transform: scale(1.02); box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_stdio=True)

# --- 2. 侧边栏：收银台与导航 ---
with st.sidebar:
    st.title("🛠️ Geng-Tools v4.0")
    st.markdown("### 💎 赞助支持")
    c1, c2 = st.columns(2)
    with c1:
        try: st.image("wx.png", caption="微信")
        except: st.caption("📸 缺失wx.png")
    with c2:
        try: st.image("ali.png", caption="支付宝")
        except: st.caption("📸 缺失ali.png")
    
    st.divider()
    menu = st.selectbox("📂 切换功能分类", [
        "🏢 办公生产力 (文件/表格)", 
        "🎨 视觉实验室 (图像处理)", 
        "📝 文字加工厂 (统计/转换)",
        "🎲 趣味与效率 (工具/随机)",
        "🩺 健康与生活 (计算/转换)"
    ])
    st.divider()
    st.info("💡 提示：所有操作均在本地浏览器处理，保护隐私安全。")

# --- 3. 功能逻辑 ---

# --- 办公生产力 ---
if menu == "🏢 办公生产力 (文件/表格)":
    tab1, tab2 = st.tabs(["📊 Excel 极速清洗", "📄 PDF 深度合并"])
    with tab1:
        file = st.file_uploader("上传 Excel", type=["xlsx"])
        if file:
            df = pd.read_excel(file)
            st.metric("数据量", f"{len(df)} 行")
            if st.button("🚀 自动对账清洗"):
                df = df.drop_duplicates().fillna(0)
                out = io.BytesIO()
                with pd.ExcelWriter(out, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                st.success("清理完成！")
                st.download_button("📥 下载成品", out.getvalue(), "cleaned.xlsx")
    with tab2:
        pdfs = st.file_uploader("上传 PDF", type="pdf", accept_multiple_files=True)
        if pdfs and st.button("🔗 合并 PDF"):
            merger = PdfWriter()
            for p in pdfs: merger.append(p)
            out = io.BytesIO()
            merger.write(out)
            st.download_button("📥 下载合并稿", out.getvalue(), "merged.pdf")

# --- 视觉实验室 ---
elif menu == "🎨 视觉实验室 (图像处理)":
    img = st.file_uploader("上传图片", type=["jpg", "png", "jpeg"])
    if img:
        image = Image.open(img)
        st.image(image, width=400)
        col1, col2 = st.columns(2)
        with col1:
            op = st.multiselect("选择滤镜/处理", ["黑白", "翻转", "底片反色", "压缩"])
        with col2:
            fmt = st.selectbox("输出格式", ["JPEG", "PNG"])
        
        if st.button("✨ 执行艺术加工"):
            if "黑白" in op: image = ImageOps.grayscale(image)
            if "翻转" in op: image = ImageOps.mirror(image)
            if "底片反色" in op: image = ImageOps.invert(image.convert("RGB"))
            out = io.BytesIO()
            q = 50 if "压缩" in op else 90
            image.convert("RGB").save(out, format=fmt, quality=q)
            st.download_button("📥 保存作品", out.getvalue(), f"result.{fmt.lower()}")

# --- 文字加工厂 ---
elif menu == "📝 文字加工厂 (统计/转换)":
    st.header("📝 文字高效处理")
    text_input = st.text_area("在此输入或粘贴长文本...", height=200)
    if text_input:
        c1, c2, c3 = st.columns(3)
        c1.metric("字符数", len(text_input))
        c2.metric("不含空格", len(text_input.replace(" ", "").replace("\n", "")))
        c3.metric("行数", len(text_input.split('\n')))
        
        if st.button("🔠 大小写一键转换"):
            st.code(text_input.upper())
            st.caption("上方为转换后的全大写文本")

# --- 趣味与效率 ---
elif menu == "🎲 趣味与效率 (工具/随机)":
    t1, t2, t3 = st.tabs(["🔗 二维码", "🔐 密码生成", "⚖️ 随机决策"])
    with t1:
        url = st.text_input("输入网址生成二维码")
        if url:
            qr = f"https://qrserver.com{url}"
            st.image(qr, "扫描即可访问")
    with t2:
        length = st.select_slider("密码复杂度", options=[8, 12, 16, 20, 32])
        if st.button("🎲 生成强密码"):
            p = ''.join(random.choice(string.ascii_letters + string.digits + "!@#$%^&*") for _ in range(length))
            st.code(p)
    with t3:
        options = st.text_input("纠结什么？输入选项用逗号隔开", "吃火锅, 吃烧烤, 吃泡面")
        if st.button("🔮 帮我选一个"):
            choice = random.choice(options.split(','))
            st.balloons()
            st.subheader(f"结果是：{choice.strip()}！")

# --- 健康与生活 ---
elif menu == "🩺 健康 with 生活 (计算/转换)":
    mode = st.radio("模式", ["BMI计算", "汇率模拟", "倒计时器"])
    if mode == "BMI计算":
        h = st.number_input("身高(cm)", 100, 250, 170)
        w = st.number_input("体重(kg)", 30, 200, 60)
        if st.button("计算"):
            bmi = round(w/((h/100)**2), 1)
            st.info(f"BMI: {bmi}")
    elif mode == "汇率模拟":
        rmb = st.number_input("输入人民币(¥)", min_value=0.0)
        st.success(f"约等于 {round(rmb * 0.14, 2)} 美元 / {round(rmb * 21.3, 2)} 日元")
    elif mode == "倒计时器":
        mins = st.number_input("分钟", 1, 60, 5)
        if st.button("开始计时"):
            ph = st.empty()
            for i in range(mins * 60, 0, -1):
                ph.subheader(f"⏳ 剩余时间：{i//60}分{i%60}秒")
                time.sleep(1)
            st.success("⏰ 时间到！")
