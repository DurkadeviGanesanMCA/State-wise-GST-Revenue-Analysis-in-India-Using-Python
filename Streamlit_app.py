import streamlit as st
import pandas as pd
import plotly.express as px

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

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.header("Filters")

selected_years = st.sidebar.multiselect(
    "Select Year",
    sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

selected_states = st.sidebar.multiselect(
    "Select State",
    sorted(df["State"].unique()),
    default=sorted(df["State"].unique())
)

filtered_df = df[
    (df["Year"].isin(selected_years)) &
    (df["State"].isin(selected_states))
]

# -----------------------------
# Title
# -----------------------------

st.title("GST Revenue Analysis Dashboard")

st.markdown("---")

# -----------------------------
# KPI Cards
# -----------------------------

total_collection = filtered["Total_GST"].sum()

cgst = filtered["CGST"].sum()

sgst = filtered["SGST"].sum()

igst = filtered["IGST"].sum()

cess = filtered["CESS"].sum()

c1,c2,c3,c4,c5 = st.columns(5)

c1.metric("Total GST", f"₹ {total_collection:,.0f}")
c2.metric("CGST", f"₹ {cgst:,.0f}")
c3.metric("SGST", f"₹ {sgst:,.0f}")
c4.metric("IGST", f"₹ {igst:,.0f}")
c5.metric("CESS", f"₹ {cess:,.0f}")

st.markdown("---")

# =============================
# Monthly Trend
# =============================

monthly = filtered.groupby("Date")["Total_GST"].sum().reset_index()

fig = px.line(
    monthly,
    x="Date",
    y="Total_GST",
    title="Monthly GST Collection Trend",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

# =============================
# State Comparison
# =============================

state = filtered.groupby("State Name")["Total_GST"].sum().reset_index()

state = state.sort_values("Total_GST", ascending=False)

fig = px.bar(
    state,
    x="State Name",
    y="Total_GST",
    title="GST Collection by State"
)

st.plotly_chart(fig, use_container_width=True)

# =============================
# GST Components
# =============================

component = pd.DataFrame({
    "Component":["CGST","SGST","IGST","CESS"],
    "Revenue":[cgst,sgst,igst,cess]
})

fig = px.pie(
    component,
    names="Component",
    values="Revenue",
    title="GST Component Contribution"
)

st.plotly_chart(fig, use_container_width=True)

# =============================
# Top & Bottom States
# =============================

left,right = st.columns(2)

top = state.head(10)

bottom = state.tail(10)

fig = px.bar(
    top,
    x="Total_GST",
    y="State Name",
    orientation="h",
    title="Top 10 Revenue States"
)

left.plotly_chart(fig, use_container_width=True)

fig = px.bar(
    bottom,
    x="Total_GST",
    y="State Name",
    orientation="h",
    title="Bottom 10 Revenue States"
)

right.plotly_chart(fig, use_container_width=True)

# =============================
# YoY Growth
# =============================

yearly = filtered.groupby("Year")["Total_GST"].sum().reset_index()

yearly["YoY %"] = yearly["Total_GST"].pct_change()*100

fig = px.bar(
    yearly,
    x="Year",
    y="YoY %",
    text_auto=".2f",
    title="Year over Year Growth (%)"
)

st.plotly_chart(fig, use_container_width=True)

# =============================
# Month over Month Growth
# =============================

mom = filtered.groupby("Date")["Total_GST"].sum().reset_index()

mom["MoM %"] = mom["Total_GST"].pct_change()*100

fig = px.line(
    mom,
    x="Date",
    y="MoM %",
    markers=True,
    title="Month over Month Growth (%)"
)

st.plotly_chart(fig, use_container_width=True)

# =============================
# Seasonal Pattern
# =============================

season = filtered.groupby("Month_Name")["Total_GST"].sum().reset_index()

months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

season["Month_Name"] = pd.Categorical(
    season["Month_Name"],
    categories=months,
    ordered=True
)

season = season.sort_values("Month_Name")

fig = px.line(
    season,
    x="Month_Name",
    y="Total_GST",
    markers=True,
    title="Seasonal Pattern"
)

st.plotly_chart(fig, use_container_width=True)

# =============================
# Heatmap (Year x Month)
# =============================

pivot = filtered.pivot_table(
    values="Total_GST",
    index="Year",
    columns="Month_Num",
    aggfunc="sum"
)

fig = px.imshow(
    pivot,
    text_auto=True,
    aspect="auto",
    title="GST Collection Heatmap"
)

st.plotly_chart(fig, use_container_width=True)

# =============================
# Anomaly Detection
# =============================

monthly = filtered.groupby("Date")["Total_GST"].sum().reset_index()

mean = monthly["Total_GST"].mean()
std = monthly["Total_GST"].std()

monthly["Anomaly"] = (
    (monthly["Total_GST"] > mean + 2*std) |
    (monthly["Total_GST"] < mean - 2*std)
)

fig = px.scatter(
    monthly,
    x="Date",
    y="Total_GST",
    color="Anomaly",
    title="GST Collection Anomaly Detection"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("GST Revenue Dashboard | Streamlit + Plotly")
