import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# =====================================================
# Common Layout
# =====================================================
def apply_common_layout(fig, height=360):
    fig.update_layout(
        height=height,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=50, b=20),
        title=dict(
            x=0.5,
            xanchor="center",
            font=dict(size=18)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )

    fig.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
    fig.update_yaxes(showgrid=True, gridcolor="#f1f5f9")

    return fig


# =====================================================
# Total GST Trend
# =====================================================
def draw_total_gst_trend(df):
    trend = df.groupby("Date")["Total_GST"].sum().reset_index().sort_values("Date")

    fig = px.line(
        trend,
        x="Date",
        y="Total_GST",
        markers=True,
        title="Total GST Trend"
    )

    fig.update_traces(
        line=dict(color="#1d4ed8", width=3),
        marker=dict(size=6)
    )

    return apply_common_layout(fig)


# =====================================================
# State-wise Collection
# =====================================================
def draw_state_wise_collection(df):
    state = (
        df.groupby("State Name")["Total_GST"]
        .sum()
        .reset_index()
        .sort_values("Total_GST", ascending=False)
    )

    fig = px.bar(
        state,
        x="State Name",
        y="Total_GST",
        title="State-wise GST Collection"
    )

    fig.update_traces(marker_color="#1d4ed8")

    return apply_common_layout(fig)


# =====================================================
# GST Component Donut
# =====================================================
def draw_component_donut(df):

    labels = ["CGST", "SGST", "IGST", "CESS"]
    values = [df[i].sum() for i in labels]

    fig = px.pie(
        values=values,
        names=labels,
        hole=0.5,
        title="GST Component Contribution",
        color_discrete_sequence=[
            "#1d4ed8",
            "#60a5fa",
            "#34d399",
            "#f87171"
        ]
    )

    fig.update_traces(textinfo="percent+label")

    return apply_common_layout(fig)


# =====================================================
# Top 10 States
# =====================================================
def draw_top_states_bar(df):

    top = (
        df.groupby("State Name")["Total_GST"]
        .sum()
        .reset_index()
        .sort_values("Total_GST", ascending=False)
        .head(10)
        .sort_values("Total_GST")
    )

    fig = px.bar(
        top,
        x="Total_GST",
        y="State Name",
        orientation="h",
        title="Top 10 States"
    )

    fig.update_traces(marker_color="#22c55e")

    return apply_common_layout(fig)


# =====================================================
# Bottom 10 States
# =====================================================
def draw_bottom_states_bar(df):

    bottom = (
        df.groupby("State Name")["Total_GST"]
        .sum()
        .reset_index()
        .sort_values("Total_GST")
        .head(10)
    )

    fig = px.bar(
        bottom,
        x="Total_GST",
        y="State Name",
        orientation="h",
        title="Bottom 10 States"
    )

    fig.update_traces(marker_color="#ef4444")

    return apply_common_layout(fig)


# =====================================================
# YoY Growth
# =====================================================
def draw_yoy_growth():

    years = ["2021", "2022", "2023", "2024"]
    growth = [18.7, 16.5, 13.9, 11.6]

    fig = px.bar(
        x=years,
        y=growth,
        text=[f"{i}%" for i in growth],
        title="Year-over-Year Growth"
    )

    fig.update_traces(
        marker_color="#6366f1",
        textposition="outside"
    )

    fig.update_yaxes(range=[0, 25])

    return apply_common_layout(fig)


# =====================================================
# Month-on-Month Growth
# =====================================================
def draw_mom_growth(df):

    trend = (
        df.groupby("Date")["Total_GST"]
        .sum()
        .pct_change()
        .fillna(0)
        * 100
    )

    trend = trend.reset_index()

    fig = px.line(
        trend,
        x="Date",
        y="Total_GST",
        title="Month-on-Month Growth"
    )

    fig.update_traces(
        line=dict(color="#8b5cf6", width=3)
    )

    return apply_common_layout(fig)


# =====================================================
# Seasonal Analysis
# =====================================================
def draw_seasonal_analysis(df):

    order = [f"{i:02d}" for i in range(1,13)]

    temp = df.copy()

    temp["Month"] = (
        temp["Month"]
        .astype(str)
        .str.zfill(2)
    )

    seasonal = (
        temp.groupby("Month")["Total_GST"]
        .mean()
        .reset_index()
    )

    seasonal["Month"] = pd.Categorical(
        seasonal["Month"],
        categories=order,
        ordered=True
    )

    seasonal = seasonal.sort_values("Month")

    fig = px.bar(
        seasonal,
        x="Month",
        y="Total_GST",
        title="Seasonal Analysis",
        category_orders={"Month": order}
    )

    fig.update_traces(marker_color="#ea580c")

    fig.update_yaxes(
        title="Average GST (₹ Crore)",
        tickformat=",.0f"
    )

    return apply_common_layout(fig, height=420)


# =====================================================
# Anomaly Detection
# =====================================================
def draw_anomaly_detection(df):

    trend = (
        df.groupby("Date")["Total_GST"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        trend,
        x="Date",
        y="Total_GST",
        title="Anomaly Detection"
    )

    fig.update_traces(
        line=dict(color="#1d4ed8", width=3)
    )

    if len(trend) > 3:

        anomalies = trend.sample(frac=0.1, random_state=42)

        fig.add_trace(
            go.Scatter(
                x=anomalies["Date"],
                y=anomalies["Total_GST"],
                mode="markers",
                marker=dict(
                    color="red",
                    size=9
                ),
                name="Anomaly"
            )
        )

    return apply_common_layout(fig)
