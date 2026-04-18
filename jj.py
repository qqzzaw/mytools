import streamlit as st
import pandas as pd
from pypdf import PdfWriter
from PIL import Image
import io

# 1. 页面设置
st.set_page_config(page_title="省心办公百宝箱", layout="wide")

# 2. 侧边栏：收款码与功能选择
with st.sidebar:
    st.title("💰 赞助支持")
    st.write("如果工具帮到了你，欢迎投喂☕")
    
    col1, col2 = st.columns(2)
    with col1:
        try: st.image("wx.png", caption="微信支付")
        except: st.write("请放wx.png")
    with col2:
        try: st.image("ali.png", caption="支付宝")
        except: st.write("请放ali.png")
            
    st.divider()
    menu = st.radio("请选择功能模块：", ["Excel 自动对账", "PDF 快速合并", "图片极简压缩"])

# --- 模块 1：Excel 自动对账 (真实逻辑) ---
if menu == "Excel 自动对账":
    st.header("📊 Excel 数据自动清洗/填充")
    st.write("功能：自动填充空值，统一格式，方便对账。")
    file = st.file_uploader("上传 Excel 文件", type=["xlsx", "xls"])
    if file:
        df = pd.read_excel(file)
        st.write("预览原始数据：", df.head())
        if st.button("🚀 开始一键处理"):
            # 真实逻辑：填充空值为0，并格式化
            df = df.fillna(0)
            st.success("处理成功！")
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            st.download_button("📥 下载处理后的 Excel", data=output.getvalue(), file_name="已对账数据.xlsx")

# --- 模块 2：PDF 快速合并 (真实逻辑) ---
elif menu == "PDF 快速合并":
    st.header("📄 PDF 极简合并工具")
    st.write("功能：将多个 PDF 按顺序合并成一个文件。")
    pdf_files = st.file_uploader("上传多个 PDF", type="pdf", accept_multiple_files=True)
    if pdf_files:
        if st.button("🚀 立即合并"):
            merger = PdfWriter()
            for pdf in pdf_files:
                merger.append(pdf)
            output = io.BytesIO()
            merger.write(output)
            st.success(f"✅ 已成功合并 {len(pdf_files)} 个文件！")
            st.download_button("📥 点击下载合并后的 PDF", data=output.getvalue(), file_name="合并文档.pdf")

# --- 模块 3：图片极简压缩 (真实逻辑) ---
elif menu == "图片极简压缩":
    st.header("🖼️ 图片批量压缩")
    st.write("功能：减小图片体积，方便传输。")
    img_file = st.file_uploader("上传图片", type=["jpg", "png", "jpeg"])
    if img_file:
        image = Image.open(img_file)
        quality = st.slider("选择压缩质量 (数字越小体积越小)", 10, 100, 70)
        if st.button("🚀 执行压缩"):
            output = io.BytesIO()
            # 统一转为 RGB 处理
            rgb_im = image.convert('RGB')
            rgb_im.save(output, format="JPEG", quality=quality)
            st.success("压缩完成！")
            st.download_button("📥 下载压缩后的图片", data=output.getvalue(), file_name="compressed.jpg")
