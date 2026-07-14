import streamlit as st
import pandas as pd
from utils import load_and_filter_data, calculate_kpis
import charts

# Page Configurations
st.set_page_config(
    page_title="GST Collection Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ingest Global Custom CSS Layout Structures
#with open("style.css") as f:
    #st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Main Data Pipeline
DATA_FILE = "cleaned_data.csv"
raw_df = pd.read_csv(DATA_FILE)

raw_df["Year"] = pd.to_datetime(raw_df["Year"]).dt.year

# Sidebar Filter Implementation Elements
st.sidebar.title("Filters")
available_years = sorted(list(raw_df['Year'].unique()))
selected_years = st.sidebar.multiselect("Select Year", available_years, default=available_years)

available_states = ["All"] + sorted(list(raw_df['State Name'].unique()))
selected_states = st.sidebar.selectbox("Select State Name", available_states, index=0)

# Filter Dataset based on selections
filtered_df = load_and_filter_data(DATA_FILE, selected_years, [selected_states] if selected_states != "All" else None)
metrics = calculate_kpis(filtered_df)

# Dashboard Title Area
# st.title("📊 GST Collection Dashboard")
st.markdown(
    """
    <h1 style="color:#0000FF; font-size:42px; font-weight:bold;">
        📊 State-Wise GST Analysis Dashboard
    </h1>
    """,
    unsafe_allow_html=True,
)

# --- Row 1: Key Performance Metrics Blocks (KPIs) ---
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    st.markdown(f'''<div class="metric-card"><div>
        <p class="metric-title">Total_GST</p>
        <p class="metric-value">₹ {metrics["total_gst"]:,} Cr</p>
    </div><span style="font-size:30px;">🔵</span></div>''', unsafe_allow_html=True)

with kpi_col2:
    st.markdown(f'''<div class="metric-card"><div>
        <p class="metric-title">Average GST</p>
        <p class="metric-value">₹ {int(metrics["avg_gst"]):,} Cr</p>
    </div><span style="font-size:30px;">📈</span></div>''', unsafe_allow_html=True)

with kpi_col3:
    st.markdown(f'''<div class="metric-card"><div>
        <p class="metric-title">Top State ({metrics["top_state"]})</p>
        <p class="metric-value">₹ {metrics["top_val"]:,} Cr</p>
    </div><span style="font-size:30px;">🏆</span></div>''', unsafe_allow_html=True)

with kpi_col4:
    st.markdown(f'''<div class="metric-card"><div>
        <p class="metric-title">Bottom State ({metrics["bottom_state"]})</p>
        <p class="metric-value">₹ {metrics["bottom_val"]:,} Cr</p>
    </div><span style="font-size:30px;">🚨</span></div>''', unsafe_allow_html=True)

# --- Row 2: Global Trends & Geographical Collection distributions ---
row2_col1, row2_col2 = st.columns([1, 1])
with row2_col1:
    st.plotly_chart(charts.draw_total_gst_trend(filtered_df), use_container_width=True)
with row2_col2:
    st.plotly_chart(charts.draw_state_wise_collection(filtered_df), use_container_width=True)

# --- Row 3: Component Structural Breakdown & State Leaderboards ---
row3_col1, row3_col2, row3_col3 = st.columns([1, 1, 1])
with row3_col1:
    st.plotly_chart(charts.draw_component_donut(filtered_df), use_container_width=True)
with row3_col2:
    st.plotly_chart(charts.draw_top_states_bar(filtered_df), use_container_width=True)
with row3_col3:
    st.plotly_chart(charts.draw_bottom_states_bar(filtered_df), use_container_width=True)

# --- Row 4: Deep Insights and Analytics Matrix ---
row4_col1, row4_col2, row4_col3, row4_col4 = st.columns(4)
with row4_col1:
    st.plotly_chart(charts.draw_yoy_growth(), use_container_width=True)
with row4_col2:
    st.plotly_chart(charts.draw_mom_growth(filtered_df), use_container_width=True)
with row4_col3:
    st.plotly_chart(charts.draw_seasonal_analysis(filtered_df), use_container_width=True)
with row4_col4:
    st.plotly_chart(charts.draw_anomaly_detection(filtered_df), use_container_width=True)

# --- Row 5: Detailed Data Ingestion Table ---
st.subheader("GST Data Ledger")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

st.markdown("<p style='text-align: center; color: gray; font-size:12px; margin-top:50px;'>GST Collection Dashboard | Developed using Streamlit & Plotly</p>", unsafe_allow_html=True)
