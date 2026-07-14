import streamlit as st
import pandas as pd
from utils import load_and_filter_data, calculate_kpis, process_advanced_analytics
import charts

st.set_page_config(page_title="GST Collection Dashboard", layout="wide")

# Read layout constraints from style sheet
try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

DATA_FILE = "gst_data.csv"
raw_df = pd.read_csv(DATA_FILE)

# Sidebar Filter Implementation
st.sidebar.title("Filters")
available_years = sorted(list(raw_df['Year'].unique()))
selected_years = st.sidebar.multiselect("Select Year", available_years, default=available_years)

available_states = ["All"] + sorted(list(raw_df['State'].unique()))
selected_states = st.sidebar.selectbox("Select State", available_states, index=0)

# Load data frameworks via processing pipelines
filtered_df = load_and_filter_data(DATA_FILE, selected_years, [selected_states] if selected_states != "All" else None)
metrics = calculate_kpis(filtered_df)
timeline_df, yoy_df, seasonal_df = process_advanced_analytics(filtered_df)

# Main Title Headers
st.title("📊 GST Collection Dashboard")
st.caption("Interactive analytical matrix for tracked GST workflows and revenue trends.")

# --- Row 1: Objective KPI Callouts ---
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
with kpi_col1:
    st.markdown(f'<div class="metric-card"><div><p class="metric-title">Total GST Collection</p><p class="metric-value">₹ {metrics["total_gst"]:,} Cr</p></div><span>🔵</span></div>', unsafe_allow_html=True)
with kpi_col2:
    st.markdown(f'<div class="metric-card"><div><p class="metric-title">Systemic Average Collection</p><p class="metric-value">₹ {int(metrics["avg_gst"]):,} Cr</p></div><span>📈</span></div>', unsafe_allow_html=True)
with kpi_col3:
    st.markdown(f'<div class="metric-card"><div><p class="metric-title">Top Performer ({metrics["top_state"]})</p><p class="metric-value">₹ {metrics["top_val"]:,} Cr</p></div><span>🏆</span></div>', unsafe_allow_html=True)
with kpi_col4:
    st.markdown(f'<div class="metric-card"><div><p class="metric-title">Bottom Performer ({metrics["bottom_state"]})</p><p class="metric-value">₹ {metrics["bottom_val"]:,} Cr</p></div><span>🚨</span></div>', unsafe_allow_html=True)

# --- Row 2: Basic Trends ---
r2_1, r2_2 = st.columns(2)
r2_1.plotly_chart(charts.draw_total_gst_trend(timeline_df), use_container_width=True)
r2_2.plotly_chart(charts.draw_state_wise_collection(filtered_df), use_container_width=True)

# --- Row 3: Component Shares and Leaderboards ---
r3_1, r3_2, r3_3 = st.columns([1, 1.2, 1.2])
r3_1.plotly_chart(charts.draw_component_donut(filtered_df), use_container_width=True)
r3_2.plotly_chart(charts.draw_top_states_bar(filtered_df), use_container_width=True)
r3_3.plotly_chart(charts.draw_bottom_states_bar(filtered_df), use_container_width=True)

# --- Row 4: Advanced Predictive & Growth Metrics ---
r4_1, r4_2, r4_3, r4_4 = st.columns(4)
r4_1.plotly_chart(charts.draw_yoy_growth(yoy_df), use_container_width=True)
r4_2.plotly_chart(charts.draw_mom_growth(timeline_df), use_container_width=True)
r4_3.plotly_chart(charts.draw_seasonal_analysis(seasonal_df), use_container_width=True)
r4_4.plotly_chart(charts.draw_anomaly_detection(timeline_df), use_container_width=True)

# --- Row 5: Tabular Data Source Verification ---
st.subheader("Audited GST Ledger Framework")
st.dataframe(filtered_df.drop(columns=['Month_Num'], errors='ignore'), use_container_width=True, hide_index=True)
