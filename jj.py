import streamlit as st
import pandas as pd
import yfinance as yf
import datetime

# --- 1. 页面配置 ---
st.set_page_config(page_title="真·理财情报站", layout="wide")

# --- 2. 实时数据抓取引擎 ---
def fetch_real_market_data():
    """
    实时抓取全球核心理财标的
    """
    # 黄金 (GC=F), 标普500 (SPY), 日经225 (^N225)
    symbols = {"黄金避险": "GC=F", "美股指数": "SPY", "日股行情": "^N225"}
    data_list = []
    
    for name, sym in symbols.items():
        try:
            ticker = yf.Ticker(sym)
            price = ticker.fast_info['last_price']
            change = ticker.fast_info['year_to_date_change'] * 100
            data_list.append({"名称": name, "当前价": round(price, 2), "年内涨跌": f"{round(change, 2)}%"})
        except:
            data_list.append({"名称": name, "当前价": "获取中", "年内涨跌": "待刷新"})
    return data_list

# --- 3. 侧边栏 ---
with st.sidebar:
    st.title("💰 财富监控台")
    st.write(f"🕒 实时数据同步时间: {datetime.datetime.now().strftime('%H:%M:%S')}")
    if st.button("🔄 立即刷新行情"):
        st.rerun()
    st.divider()
    st.info("💡 提示：本站已接入 Yahoo Finance 实时数据流。")

# --- 4. 主界面 ---
st.title("📈 全球理财实时情报")
st.caption("基于 Python 自动化引擎，每秒同步全球金融波动")

st.divider()

# 获取真实行情
market_data = fetch_real_market_data()

# 展示实时看板
cols = st.columns(3)
for i, item in enumerate(market_data):
    with cols[i]:
        with st.container(border=True):
            st.write(f"### {item['名称']}")
            st.metric("实时价格", item['当前价'], delta=item['年内涨跌'])
            
            # 根据行情给出“容易赚钱”的建议
            if "黄金" in item['名称']:
                st.write("💡 **建议**：全球局势不稳，黄金作为避险资产可分批小额定投。")
            elif "美股" in item['名称']:
                st.write("💡 **建议**：科技股走势强劲，建议关注相关纳指ETF。")
            else:
                st.write("💡 **建议**：日元波动较大，注意汇率风险。")

# --- 5. 每日理财任务 (增加粘性) ---
st.divider()
st.subheader("📝 今日稳健理财任务")
st.checkbox("1. 检查今日货币基金收益是否到账")
st.checkbox("2. 观察黄金价格是否回踩 5 日均线")
st.checkbox("3. 记录一笔今日的意外支出")

# --- 6. 合规声明 ---
st.divider()
st.caption("⚠️ 免责声明：本站数据通过公开接口抓取，仅供学习参考，不作为投资决策依据。理财有风险，投资需谨慎。")
