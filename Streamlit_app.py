import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ******************** Page Configuration ***********************

st.set_page_config(
    page_title="GST Tax Collection Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    # Reads the dataset and correctly parses the 'Date' column
    df = pd.read_csv("cleaned_data.csv")
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df["Month_Name"] = df["Date"].dt.strftime("%b")
    df["Month_Num"] = df["Date"].dt.month
    
    # Overwrites the raw placeholders to create clean sorting/filtering keys
    df["Year"] = df["Date"].dt.year
 
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Please ensure your dataset is named 'cleaned_data.csv' and placed in the same directory.")
    st.stop()

st.title("📊 GST TAX Collection Dashboard")
st.markdown("Interactive analysis of GST collections across States and Union Territories.")


# Sidebar Filters

st.sidebar.header("Filters")

# Extract unique configuration values
unique_years = sorted(df["Year"].unique())
unique_states = sorted(df["State Name"].unique())

# Setup multiselect values with safe fallbacks
year = st.sidebar.multiselect(
    "Select Year", 
    unique_years, 
    default=unique_years
)
state = st.sidebar.multiselect(
    "Select State", 
    unique_states, 
    default=unique_states
)

# Robust bitwise logic matching fallback filters if empty lists are passed
filtered_df = df[
    (df["Year"].isin(year if year else unique_years)) & 
    (df["State Name"].isin(state if state else unique_states))
]

# KPI Metrics

if not filtered_df.empty:
    total_gst = filtered_df["Total_GST"].sum()
    avg_gst = filtered_df["Total_GST"].mean()
    top_state = filtered_df.groupby("State Name")["Total_GST"].sum().idxmax()
    bottom_state = filtered_df.groupby("State Name")["Total_GST"].sum().idxmin()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total GST", f"₹ {total_gst:,.2f} Cr")
    c2.metric("Average GST", f"₹ {avg_gst:,.2f} Cr")
    c3.metric("Top State", top_state)
    c4.metric("Bottom State", bottom_state)
else:
    st.warning("No records match current filtering parameters.")
    st.stop()

# Total GST Trend

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


# State-wise GST Collection

st.subheader("State-wise GST Collection")
state_data = (
    filtered_df.groupby("State Name")["Total_GST"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
fig = px.bar(
    state_data, 
    x="State Name", 
    y="Total_GST", 
    color="Total_GST",
    title="Cumulative Collection by Region"
)
st.plotly_chart(fig, use_container_width=True)


# GST Component Contribution

st.subheader("GST Component Contribution")
# Columns synchronized directly with uppercase CESS flag
components = filtered_df[["CGST", "SGST", "IGST", "CESS"]].sum()
fig = px.pie(
    names=components.index, 
    values=components.values, 
    hole=0.4,
    title="Distribution of Collection Components"
)
st.plotly_chart(fig, use_container_width=True)


# Top & Bottom Revenue States

col1, col2 = st.columns(2)
with col1:
    st.subheader("Top 10 States")
    top10 = state_data.head(10)
    fig = px.bar(
        top10, 
        x="Total_GST", 
        y="State Name", 
        orientation="h",
        category_orders={"State Name": top10["State Name"].tolist()[::-1]}
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Bottom 10 States")
    bottom10 = state_data.tail(10)
    fig = px.bar(
        bottom10, 
        x="Total_GST", 
        y="State Name", 
        orientation="h",
        category_orders={"State Name": bottom10["State Name"].tolist()[::-1]}
    )
    st.plotly_chart(fig, use_container_width=True)


#  Year-over-Year Growth

st.subheader("Year-over-Year Growth")
yoy = filtered_df.groupby("Year")["Total_GST"].sum().reset_index()
yoy["YoY Growth %"] = yoy["Total_GST"].pct_change() * 100
fig = px.bar(
    yoy, 
    x="Year", 
    y="YoY Growth %",
    title="Annual Relative Performance Percentage"
)
st.plotly_chart(fig, use_container_width=True)


# Month-over-Month Growth

st.subheader("Month-over-Month Growth")
mom = trend.copy()
mom["MoM Growth %"] = mom["Total_GST"].pct_change() * 100
fig = px.line(
    mom, 
    x="Date", 
    y="MoM Growth %", 
    markers=True,
    title="Sequential Performance Progression Delta"
)
st.plotly_chart(fig, use_container_width=True)

# Seasonal Analysis

st.subheader("Seasonal Analysis")
# Grouping via calculated values avoids errors from raw datetime parameters
season = (
    filtered_df.groupby(["Month_Num", "Month_Name"])["Total_GST"]
    .mean()
    .reset_index()
    .sort_values("Month_Num")
)
fig = px.bar(
    season, 
    x="Month_Name", 
    y="Total_GST",
    title="Average Monthly Performance Across Years"
)
st.plotly_chart(fig, use_container_width=True)


# Anomaly Detection

st.subheader("Anomalies & Deviations")
if len(trend) > 1:
    mean_val = trend["Total_GST"].mean()
    std_val = trend["Total_GST"].std()
    
    # Check if calculation is viable (avoids division by zero/NaN triggers)
    std_val = std_val if std_val > 0 else 1.0
    trend["Anomaly"] = (abs(trend["Total_GST"] - mean_val) > 2 * std_val)
    
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=trend["Date"], 
            y=trend["Total_GST"], 
            mode="lines+markers", 
            name="Normal Stream"
        )
    )
    anomalies = trend[trend["Anomaly"]]
    fig.add_trace(
        go.Scatter(
            x=anomalies["Date"], 
            y=anomalies["Total_GST"], 
            mode="markers", 
            marker=dict(color="crimson", size=11, symbol="x"), 
            name="Outlier Alert (>2σ)"
        )
    )
    fig.update_layout(title="Statistical Revenue Outliers")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Insufficient longitudinal data points to generate threshold deviation bounds.")



# ==========================================
# Interactive Data Table
# ==========================================
st.subheader("Raw Aggregated Data Matrix")
st.dataframe(filtered_df, use_container_width=True)


