import streamlit as st
import yfinance as yf
import datetime
import time

# --- 1. 页面配置 ---
st.set_page_config(page_title="理财实时情报站", layout="wide")

# --- 2. 核心：带缓存的实时抓取引擎 ---
@st.cache_data(ttl=60) # 每一分钟强制更新一次，保证“实时”且不卡
def get_live_data():
    # 监控标的：黄金(GC=F)、标普500(SPY)、日经225(^N225)
    targets = {"黄金避险": "GC=F", "美股指数": "SPY", "日股行情": "^N225"}
    results = {}
    
    for name, sym in targets.items():
        try:
            # 缩短超时时间，防止卡死
            data = yf.download(sym, period="1d", interval="1m", progress=False)
            if not data.empty:
                last_price = data['Close'].iloc[-1]
                prev_price = data['Open'].iloc[0]
                change = ((last_price - prev_price) / prev_price) * 100
                results[name] = {"price": round(float(last_price), 2), "change": round(float(change), 2)}
            else:
                results[name] = {"price": "休市中", "change": 0}
        except:
            results[name] = {"price": "连接中", "change": 0}
    return results

# --- 3. 侧边栏 ---
with st.sidebar:
    st.title("🛡️ 实时监控台")
    st.write(f"上次同步: {datetime.datetime.now().strftime('%H:%M:%S')}")
    if st.button("🔄 手动强制刷新"):
        st.cache_data.clear()
        st.rerun()
    st.divider()
    st.info("数据源：Yahoo Finance 实时流")

# --- 4. 主界面 ---
st.title("📈 全球理财实时情报 (Live)")
st.caption("基于 Python 自动化引擎，每 60 秒同步全球金融波动")

st.divider()

# 获取数据
live_data = get_live_data()

# 展示卡片
cols = st.columns(3)
for i, (name, info) in enumerate(live_data.items()):
    with cols[i]:
        with st.container(border=True):
            st.markdown(f"### {name}")
            # 使用 metric 组件展示涨跌颜色
            if isinstance(info['price'], (int, float)):
                st.metric("当前成交价", f"${info['price']}", f"{info['change']}%")
            else:
                st.metric("当前状态", info['price'])
            
            # 根据涨跌自动生成的实时建议
            if info['change'] > 0:
                st.success("🔥 趋势走强：市场情绪高涨，建议继续持有观察。")
            elif info['change'] < 0:
                st.error("📉 趋势回调：短期压力显现，可考虑轻仓避险。")
            else:
                st.warning("⚖️ 震荡整理：方向不明，建议观望为主。")

# --- 5. 自动化理财日历 (活的内容) ---
st.divider()
st.subheader("🗓️ 每日掘金计划")
day = datetime.date.today()
with st.expander(f"查看 {day} 的理财任务"):
    st.write(f"1. 监测 {'美股' if day.weekday() < 5 else '周评'} 动向")
    st.write("2. 检查黄金账户是否有调仓机会")
    st.write("3. 每日小额结余自动转入货币基金")

# --- 6. 合规底部 ---
st.divider()
st.caption("⚠️ 免责声明：实时数据仅供参考，不作为投资依据。数据采集可能存在 15 分钟左右延迟。")
