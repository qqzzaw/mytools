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

# --- 2. 侧边栏：收银台与导航 ---
with st.sidebar:
    st.title("🛠️ Geng-Tools v4.5")
    st.markdown("### 💎 赞助支持")
    c1, col2 = st.columns(2)
    with c1:
        try: st.image("wx.png", caption="微信")
        except: st.caption("📸 缺失wx.png")
    with col2:
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
    st.info("💡 提示：所有操作均在本地处理，保护隐私。")

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
        op = st.multiselect("选择滤镜/处理", ["黑白", "翻转", "压缩"])
        if st.button("✨ 执行加工"):
            if "黑白" in op: image = ImageOps.grayscale(image)
            if "翻转" in op: image = ImageOps.mirror(image)
            out = io.BytesIO()
            q = 50 if "压缩" in op else 90
            image.convert("RGB").save(out, format="JPEG", quality=q)
            st.download_button("📥 保存作品", out.getvalue(), "result.jpg")

# --- 文字加工厂 ---
elif menu == "📝 文字加工厂 (统计/转换)":
    st.header("📝 文字高效处理")
    text_input = st.text_area("在此输入或粘贴长文本...", height=200)
    if text_input:
        c1, c2, c3 = st.columns(3)
        c1.metric("字符数", len(text_input))
        c2.metric("不含空格", len(text_input.replace(" ", "").replace("\n", "")))
        c3.metric("行数", len(text_input.count('\n') + 1))
        if st.button("🔠 转为全大写"):
            st.code(text_input.upper())

# --- 趣味与效率 ---
elif menu == "🎲 趣味与效率 (工具/随机)":
    t1, t2, t3 = st.tabs(["🔗 二维码", "🔐 密码生成", "⚖️ 随机决策"])
    with t1:
        url = st.text_input("输入网址生成二维码")
        if url:
            qr = f"https://qrserver.com{url}"
            st.image(qr, "扫描访问")
    with t2:
        # --- 修复后的代码 ---
        length = st.select_slider("密码长度", options=[8, 12, 16, 24, 32])
        if st.button("🎲 生成强密码"):
            p = ''.join(random.choice(string.ascii_letters + string.digits + "!@#$%^&*") for _ in range(length))
            st.code(p)
    with t3:
        options = st.text_input("输入选项用逗号隔开", "吃火锅, 吃烧烤, 喝奶茶")
        if st.button("🔮 帮我选一个"):
            choice = random.choice(options.split(','))
            st.balloons()
            st.subheader(f"结果是：{choice.strip()}！")

# --- 健康与生活 ---
elif menu == "🩺 健康与生活 (计算/转换)":
    mode = st.radio("功能", ["BMI计算", "单位转换", "倒计时"])
    if mode == "BMI计算":
        h = st.number_input("身高(cm)", 100, 250, 170)
        w = st.number_input("体重(kg)", 30, 200, 60)
        if st.button("计算"):
            bmi = round(w/((h/100)**2), 1)
            st.info(f"您的 BMI 为: {bmi}")
    elif mode == "单位转换":
        val = st.number_input("数值", value=1.0)
        unit = st.selectbox("转换类型", ["公里 转 英里", "公斤 转 磅", "摄氏度 转 华氏度"])
        if unit == "公里 转 英里": st.write(f"{val} 公里 = {round(val*0.621, 2)} 英里")
        elif unit == "公斤 转 磅": st.write(f"{val} 公斤 = {round(val*2.204, 2)} 磅")
        elif unit == "摄氏度 转 华氏度": st.write(f"{val} °C = {round(val*1.8+32, 2)} °F")
    elif mode == "倒计时":
        mins = st.number_input("分钟", 1, 60, 5)
        if st.button("开始计时"):
            ph = st.empty()
            for i in range(mins * 60, -1, -1):
                ph.subheader(f"⏳ 剩余时间：{i//60}分{i%60}秒")
                time.sleep(1)
            st.success("⏰ 时间到！")
