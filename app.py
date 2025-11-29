import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# -------- تنظیمات صفحه --------
st.set_page_config(
    page_title="Glass Bottle Factory Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------- استایل اختصاصی --------
st.markdown("""
<style>
body {background-color: #F6F8FA;}
.block-container {padding-top: 1rem;}
.metric-container {
    background-color: white;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0px 0px 8px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# -------- ساخت دیتای نمونه کارخانه --------
np.random.seed(42)

dates = pd.date_range("2024-01-01", periods=180)

df = pd.DataFrame({
    "Date": np.tile(dates, 3),
    "Line": np.repeat(["Line 1", "Line 2", "Line 3"], len(dates)),
    "Produced Bottles": np.random.randint(8000, 14000, len(dates) * 3),
    "Rejected Bottles": np.random.randint(100, 600, len(dates) * 3),
    "Energy Consumption (kWh)": np.random.randint(4000, 9000, len(dates) * 3),
    "Downtime (hours)": np.random.uniform(0.5, 5, len(dates) * 3)
})

df["Good Bottles"] = df["Produced Bottles"] - df["Rejected Bottles"]
df["Efficiency %"] = (df["Good Bottles"] / df["Produced Bottles"] * 100)

# -------- فیلتر سایدبار --------
st.sidebar.title("⚙ فیلترها")

selected_line = st.sidebar.selectbox("انتخاب خط تولید", df["Line"].unique())
date_range = st.sidebar.date_input("بازه زمانی", [df["Date"].min(), df["Date"].max()])

filtered = df[
    (df["Line"] == selected_line) &
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1]))
]

# -------- عنوان --------
st.title("🏭 داشبورد مدیریتی کارخانه بطری شیشه‌ای")

# -------- KPI ها --------
col1, col2, col3, col4 = st.columns(4)

col1.metric("کل تولید", f"{int(filtered['Produced Bottles'].sum()):,}")
col2.metric("تولید سالم", f"{int(filtered['Good Bottles'].sum()):,}")
col3.metric("ضایعات", f"{int(filtered['Rejected Bottles'].sum()):,}")
col4.metric("بهره‌وری میانگین", f"{filtered['Efficiency %'].mean():.2f} %")

st.markdown("---")

# -------- نمودار تولید --------
fig_prod = px.line(
    filtered,
    x="Date",
    y="Produced Bottles",
    title="📈 روند تولید بطری",
    markers=True
)
st.plotly_chart(fig_prod, use_container_width=True)

# -------- نمودار ضایعات --------
colA, colB = st.columns(2)

with colA:
    fig_reject = px.bar(
        filtered,
        x="Date",
        y="Rejected Bottles",
        title="❌ میزان ضایعات روزانه",
        color="Rejected Bottles",
        color_continuous_scale="Reds"
    )
    st.plotly_chart(fig_reject, use_container_width=True)

with colB:
    fig_eff = px.area(
        filtered,
        x="Date",
        y="Efficiency %",
        title="⚡ نرخ بهره‌وری",
        color_discrete_sequence=["green"]
    )
    st.plotly_chart(fig_eff, use_container_width=True)

# -------- مصرف انرژی --------
st.subheader("🔌 مصرف انرژی خط تولید")

fig_energy = px.line(
    filtered,
    x="Date",
    y="Energy Consumption (kWh)",
    title="مصرف انرژی (kWh)",
    markers=True
)
st.plotly_chart(fig_energy, use_container_width=True)

# -------- ارتباط توقف خط و ضایعات --------
st.subheader("🚨 توقف تولید در مقابل ضایعات")

fig_scatter = px.scatter(
    filtered,
    x="Downtime (hours)",
    y="Rejected Bottles",
    size="Produced Bottles",
    color="Efficiency %",
    title="تحلیل توقف خط تولید",
    size_max=40
)
st.plotly_chart(fig_scatter, use_container_width=True)

# -------- جدول داده --------
with st.expander("📋 نمایش داده خام"):
    st.dataframe(filtered, use_container_width=True)

st.success("داشبورد با موفقیت بارگذاری شد ✅")
