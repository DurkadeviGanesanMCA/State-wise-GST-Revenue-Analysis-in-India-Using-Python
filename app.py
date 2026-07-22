import streamlit as st
import pandas as pd
from utils import load_and_filter_data, calculate_kpis
import charts

# ==========================================================
# Page Configuration
# ==========================================================
st.set_page_config(
    page_title="GST Collection Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# Dashboard Spacing
# ==========================================================
st.markdown("""
<style>
.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
    padding-left:2rem;
    padding-right:2rem;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# Load Data
# ==========================================================
DATA_FILE = "cleaned_data.csv"

raw_df = pd.read_csv(DATA_FILE)
raw_df["Year"] = pd.to_datetime(raw_df["Year"]).dt.year

# ==========================================================
# Sidebar Filters
# ==========================================================
st.sidebar.title("Filters")

available_years = sorted(raw_df["Year"].unique())
selected_years = st.sidebar.multiselect(
    "Select Year",
    available_years,
    default=available_years
)

available_states = ["All"] + sorted(raw_df["State Name"].unique())

selected_state = st.sidebar.selectbox(
    "Select State",
    available_states
)

filtered_df = load_and_filter_data(
    DATA_FILE,
    selected_years,
    [selected_state] if selected_state != "All" else None
)

metrics = calculate_kpis(filtered_df)

# ==========================================================
# Dashboard Title
# ==========================================================
st.markdown(
    """
    <h1 style="text-align:center;
               color:#1d4ed8;
               font-size:42px;
               font-weight:bold;">
        📊 State-Wise GST Analysis Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# KPI SECTION
# ==========================================================
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "Total GST",
        f"₹ {metrics['total_gst']:,} Cr"
    )

with kpi2:
    st.metric(
        "Average GST",
        f"₹ {int(metrics['avg_gst']):,} Cr"
    )

with kpi3:
    st.metric(
        f"Top State ({metrics['top_state']})",
        f"₹ {metrics['top_val']:,} Cr"
    )

with kpi4:
    st.metric(
        f"Bottom State ({metrics['bottom_state']})",
        f"₹ {metrics['bottom_val']:,} Cr"
    )

st.divider()

# ==========================================================
# Row 2 : GST Components & Rankings
# ==========================================================
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.plotly_chart(
        charts.draw_component_donut(filtered_df),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        charts.draw_top_states_bar(filtered_df),
        use_container_width=True
    )

with col3:
    st.plotly_chart(
        charts.draw_bottom_states_bar(filtered_df),
        use_container_width=True
    )

st.divider()

# ==========================================================
# Row 3 : Trends
# ==========================================================
col4, col5 = st.columns(2, gap="medium")

with col4:
    st.plotly_chart(
        charts.draw_total_gst_trend(filtered_df),
        use_container_width=True
    )

with col5:
    st.plotly_chart(
        charts.draw_state_wise_collection(filtered_df),
        use_container_width=True
    )

st.divider()

# ==========================================================
# Row 4 : Advanced Analytics
# ==========================================================
col6, col7, col8 = st.columns(3, gap="medium")

with col6:
    st.plotly_chart(
        charts.draw_yoy_growth(),
        use_container_width=True
    )

with col7:
    st.plotly_chart(
        charts.draw_mom_growth(filtered_df),
        use_container_width=True
    )

with col8:
    st.plotly_chart(
        charts.draw_anomaly_detection(filtered_df),
        use_container_width=True
    )

st.divider()

# ==========================================================
# Row 5 : Seasonal Analysis
# ==========================================================
st.plotly_chart(
    charts.draw_seasonal_analysis(filtered_df),
    use_container_width=True
)

st.divider()

# ==========================================================
# Row 6 : Data Table
# ==========================================================
st.subheader("GST Data Ledger")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# Footer
# ==========================================================
st.markdown(
    """
    <p style="text-align:center;
              color:gray;
              font-size:12px;
              margin-top:30px;">
        GST Collection Dashboard | Developed using Streamlit & Plotly
    </p>
    """,
    unsafe_allow_html=True
)
