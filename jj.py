import streamlit as st
import pandas as pd
from pypdf import PdfWriter, PdfReader
from PIL import Image
import io

# 1. 页面配置
st.set_page_config(page_title="省心办公百宝箱-增强版", layout="wide")

# 2. 侧边栏：收款码与功能选择
with st.sidebar:
    st.title("💰 赞助支持")
    st.write("工具持续更新，感谢投喂☕")
    col1, col2 = st.columns(2)
    with col1:
        try: st.image("wx.png", caption="微信支付")
        except: st.write("请放wx.png")
    with col2:
        try: st.image("ali.png", caption="支付宝")
        except: st.write("请放ali.png")
    st.divider()
    menu = st.radio("请选择功能：", ["Excel 智能对比/清洗", "PDF 合并与拆分", "图片压缩与转换"])

# --- 模块 1：Excel 智能对比/清洗 ---
if menu == "Excel 智能对比/清洗":
    st.header("📊 Excel 智能助手")
    tab1, tab2 = st.tabs(["一键清洗(填补空值)", "双表数据对比"])
    
    with tab1:
        file = st.file_uploader("上传 Excel", type=["xlsx", "xls"], key="clean")
        if file and st.button("开始清洗"):
            df = pd.read_excel(file).fillna(0)
            output = io.BytesIO()
            df.to_excel(output, index=False)
            st.download_button("📥 下载清洗后的表", data=output.getvalue(), file_name="cleaned.xlsx")
            
    with tab2:
        st.write("上传两个表，自动找出第一个表里哪些行在第二个表里没有（或金额不同）。")
        f1 = st.file_uploader("上传表 A (基准表)", type=["xlsx"])
        f2 = st.file_uploader("上传表 B (对比表)", type=["xlsx"])
        if f1 and f2 and st.button("开始对比"):
            df1, df2 = pd.read_excel(f1), pd.read_excel(f2)
            # 简单对比：找出df1中不在df2中的数据
            diff = pd.concat([df1, df2]).drop_duplicates(keep=False)
            st.write("发现差异数据：", diff)
            output = io.BytesIO()
            diff.to_excel(output, index=False)
            st.download_button("📥 下载差异报告", data=output.getvalue(), file_name="diff.xlsx")

# --- 模块 2：PDF 合并与拆分 ---
elif menu == "PDF 合并与拆分":
    st.header("📄 PDF 增强助手")
    mode = st.selectbox("选择模式：", ["合并多个PDF", "拆分单个PDF"])
    
    if mode == "合并多个PDF":
        files = st.file_uploader("上传多个 PDF", type="pdf", accept_multiple_files=True)
        if files and st.button("开始合并"):
            merger = PdfWriter()
            for f in files: merger.append(f)
            output = io.BytesIO()
            merger.write(output)
            st.download_button("📥 下载合并后的 PDF", data=output.getvalue(), file_name="combined.pdf")
            
    else:
        file = st.file_uploader("上传单个 PDF", type="pdf")
        if file:
            reader = PdfReader(file)
            st.write(f"该文件共有 {len(reader.pages)} 页")
            page_num = st.number_input("请输入你想提取的页码：", min_value=1, max_value=len(reader.pages), value=1)
            if st.button("提取该页"):
                writer = PdfWriter()
                writer.add_page(reader.pages[page_num-1])
                output = io.BytesIO()
                writer.write(output)
                st.download_button(f"📥 下载第 {page_num} 页", data=output.getvalue(), file_name="extracted.pdf")

# --- 模块 3：图片压缩与转换 ---
elif menu == "图片压缩与转换":
    st.header("🖼️ 图片转换助手")
    img_file = st.file_uploader("上传图片", type=["jpg", "png", "jpeg", "webp"])
    if img_file:
        img = Image.open(img_file)
        target_format = st.selectbox("转换目标格式：", ["JPEG", "PNG", "WEBP"])
        quality = st.slider("压缩质量：", 10, 100, 80)
        if st.button("开始转换并压缩"):
            output = io.BytesIO()
            img = img.convert("RGB") if target_format == "JPEG" else img
            img.save(output, format=target_format, quality=quality)
            st.download_button(f"📥 下载 {target_format} 图片", data=output.getvalue(), file_name=f"processed.{target_format.lower()}")
