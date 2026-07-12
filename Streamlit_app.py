import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# ******************** Page Configuration ***********************
# ==========================================
st.set_page_config(
    page_title="GST Collection Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv")

    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df["Year"] = df["Date"].dt.year
    df["Month_Name"] = df["Date"].dt.strftime("%b")
    df["Month_Num"] = df["Date"].dt.month

    return df

df = load_data()


st.title("📊 GST Collection Dashboard")
st.markdown("Interactive analysis of GST collections across States and Union Territories.")

# ==========================================
# Sidebar Filters
# ==========================================
st.sidebar.header("Filters")

year = st.sidebar.multiselect(
    "Select Year",
    sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

state = st.sidebar.multiselect(
    "Select State",
    sorted(df["State"].unique()),
    default=sorted(df["State"].unique())
)

filtered_df = df[
    (df["Year"].isin(year)) &
    (df["State"].isin(state))
]

# ==========================================
# KPI Metrics
# ==========================================

total_gst = filtered_df["Total_GST"].sum()
avg_gst = filtered_df["Total_GST"].mean()

top_state = (
    filtered_df.groupby("State")["Total_GST"]
    .sum()
    .idxmax()
)

bottom_state = (
    filtered_df.groupby("State")["Total_GST"]
    .sum()
    .idxmin()
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total GST", f"₹ {total_gst:,.0f}")
c2.metric("Average GST", f"₹ {avg_gst:,.0f}")
c3.metric("Top State", top_state)
c4.metric("Bottom State", bottom_state)

# ==========================================
# Total GST Trend
# ==========================================

st.subheader("Total GST Trend")

trend = filtered_df.groupby("Date")["Total_GST"].sum().reset_index()

fig = px.line(
    trend,
    x="Date",
    y="Total_GST",
    markers=True,
    title="GST Collection Over Time"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# State-wise GST Collection
# ==========================================

st.subheader("State-wise GST Collection")

state_data = (
    filtered_df.groupby("State")["Total_GST"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    state_data,
    x="State",
    y="Total_GST",
    color="Total_GST"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# GST Component Contribution
# ==========================================

st.subheader("GST Component Contribution")

components = filtered_df[
    ["CGST","SGST","IGST","Cess"]
].sum()

fig = px.pie(
    names=components.index,
    values=components.values,
    hole=0.4
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Top & Bottom Revenue States
# ==========================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("Top 10 States")

    top10 = state_data.head(10)

    fig = px.bar(
        top10,
        x="Total_GST",
        y="State",
        orientation="h"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    st.subheader("Bottom 10 States")

    bottom10 = state_data.tail(10)

    fig = px.bar(
        bottom10,
        x="Total_GST",
        y="State",
        orientation="h"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Year-over-Year Growth
# ==========================================

st.subheader("Year-over-Year Growth")

yoy = filtered_df.groupby("Year")["Total_GST"].sum().reset_index()

yoy["YoY Growth %"] = yoy["Total_GST"].pct_change()*100

fig = px.bar(
    yoy,
    x="Year",
    y="YoY Growth %"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Month-over-Month Growth
# ==========================================

st.subheader("Month-over-Month Growth")

mom = trend.copy()

mom["MoM Growth %"] = mom["Total_GST"].pct_change()*100

fig = px.line(
    mom,
    x="Date",
    y="MoM Growth %",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Seasonal Analysis
# ==========================================

st.subheader("Seasonal Analysis")

season = (
    filtered_df.groupby("Month")["Total_GST"]
    .mean()
    .reset_index()
)

fig = px.bar(
    season,
    x="Month",
    y="Total_GST"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Anomaly Detection
# ==========================================

st.subheader("Anomaly Detection")

mean = trend["Total_GST"].mean()
std = trend["Total_GST"].std()

trend["Anomaly"] = (
    abs(trend["Total_GST"] - mean) > 2 * std
)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=trend["Date"],
        y=trend["Total_GST"],
        mode="lines+markers",
        name="GST"
    )
)

fig.add_trace(
    go.Scatter(
        x=trend[trend["Anomaly"]]["Date"],
        y=trend[trend["Anomaly"]]["Total_GST"],
        mode="markers",
        marker=dict(color="red", size=10),
        name="Anomaly"
    )
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Forecasting (Optional)
# ==========================================

st.subheader("Forecasting")

st.info("Forecasting section can be implemented using Prophet, ARIMA, or another time-series model.")

# ==========================================
# Interactive Data Table
# ==========================================

st.subheader("GST Data")

st.dataframe(filtered_df, use_container_width=True)

# ==========================================
# Footer
# ==========================================

st.markdown("---")
st.caption("GST Collection Dashboard | Developed using Streamlit & Plotly")
