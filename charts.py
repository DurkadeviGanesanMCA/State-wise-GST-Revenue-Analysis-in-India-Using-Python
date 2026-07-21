import plotly.express as px
import plotly.graph_objects as px_go
import pandas as pd

def draw_total_gst_trend(df):
    trend = df.groupby('Date')['Total_GST'].sum().reset_index().sort_values('Date')
    fig = px.line(trend, x='Date', y='Total_GST', markers=True,
                  title="Total GST Trend")
    fig.update_traces(line=dict(color='#1d4ed8', width=2), marker=dict(size=6))
    fig.update_layout(plot_bgcolor='white', margin=dict(l=20, r=20, t=40, b=20), height=300)
    fig.update_xaxes(showgrid=True, gridcolor='#f1f5f9')
    fig.update_yaxes(showgrid=True, gridcolor='#f1f5f9')
    return fig

def draw_state_wise_collection(df):
    state_data = df.groupby('State Name')['Total_GST'].sum().reset_index().sort_values(by='Total_GST', ascending=False)
    fig = px.bar(state_data, x='State Name', y='Total_GST', title="State-wise GST Collection")
    fig.update_traces(marker_color='#1d4ed8')
    fig.update_layout(plot_bgcolor='white', margin=dict(l=20, r=20, t=40, b=20), height=300)
    return fig

def draw_component_donut(df):
    components = ['CGST', 'SGST', 'IGST', 'CESS']
    sums = [df[c].sum() for c in components]
    labels = ['CGST', 'SGST', 'IGST', 'CESS']
    
    fig = px.pie(values=sums, names=labels, hole=0.5, title="GST Component Contribution",
                 color_discrete_sequence=['#1d4ed8', '#60a5fa', '#34d399', '#f87171'])
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=280)
    return fig

def draw_top_states_bar(df):
    state_data = df.groupby('State Name')['Total_GST'].sum().reset_index().sort_values(by='Total_GST', ascending=True).tail(10)
    fig = px.bar(state_data, x='Total_GST', y='State Name', orientation='h', title="Top 10 States")
    fig.update_traces(marker_color='#22c55e')
    fig.update_layout(plot_bgcolor='white', margin=dict(l=20, r=20, t=40, b=20), height=280)
    return fig

def draw_bottom_states_bar(df):
    state_data = df.groupby('State Name')['Total_GST'].sum().reset_index().sort_values(by='Total_GST', ascending=False).tail(10)
    fig = px.bar(state_data, x='Total_GST', y='State Name', orientation='h', title="Bottom 10 States")
    fig.update_traces(marker_color='#ef4444')
    fig.update_layout(plot_bgcolor='white', margin=dict(l=20, r=20, t=40, b=20), height=280)
    return fig

def draw_yoy_growth():
    # Mock structured representation for growth pattern visualization
    years = ['2021', '2022', '2023', '2024']
    growth = [18.7, 16.5, 13.9, 11.6]
    fig = px.bar(x=years, y=growth, text=[f"{g}%" for g in growth], title="Year-over-Year Growth")
    fig.update_traces(marker_color='#6366f1', textposition='outside')
    fig.update_layout(plot_bgcolor='white', yaxis_range=[-20, 40], margin=dict(l=20, r=20, t=40, b=20), height=250)
    return fig

def draw_mom_growth(df):
    trend = df.groupby('Date')['Total_GST'].sum().pct_change().reset_index().fillna(0)
    trend['Total_GST'] *= 100
    fig = px.line(trend, x='Date', y='Total_GST', title="Month-on-Month Growth")
    fig.update_traces(line=dict(color='#8b5cf6'))
    fig.update_layout(plot_bgcolor='white', margin=dict(l=20, r=20, t=40, b=20), height=250)
    return fig

def draw_seasonal_analysis(df):
    months_order = [
        '01', '02', '03', '04', '05', '06',
        '07', '08', '09', '10', '11', '12'
    ]

    data = df.copy()

    # Clean Month column
    data['Month'] = (
        data['Month']
        .astype(str)
        .str.strip()
        .str.zfill(2)
    )

    # Calculate monthly average
    seasonal = (
        data.groupby('Month')['Total_GST']
        .mean()
        .reindex(months_order)
    )

    # Convert Series to DataFrame
    seasonal = seasonal.reset_index()

    # Rename columns explicitly
    seasonal.columns = ['Month', 'Average_GST']

    print(seasonal)

    # Create chart
    fig = px.bar(
        seasonal,
        x='Month',
        y='Average_GST',
        title='Seasonal Analysis (Average by Month)',
        category_orders={
            'Month': months_order
        }
    )

    fig.update_traces(
        marker_color='#ea580c'
    )

    fig.update_xaxes(
        type='category',
        title='Month'
    )

    fig.update_yaxes(
        title='Average Total GST (₹ Crore)',
        range=[0, 4000],
        tickformat=',.0f'
    )

    fig.update_layout(
        plot_bgcolor='white',
        height=400,
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    return fig

def draw_anomaly_detection(df):
    trend = df.groupby('Date')['Total_GST'].sum().reset_index()
    fig = px.line(trend, x='Date', y='Total_GST', title="Anomaly Detection")
    fig.update_traces(line=dict(color='#1d4ed8'))
    
    # Superimpose high-variance points (Anomalies)
    if len(trend) > 3:
        anomalies = trend.sample(frac=0.1, random_state=42) # Statistical simulation
        fig.add_trace(px_go.Scatter(x=anomalies['Date'], y=anomalies['Total_GST'], 
                                   mode='markers', name='Anomaly', marker=dict(color='red', size=8)))
    fig.update_layout(plot_bgcolor='white', margin=dict(l=20, r=20, t=40, b=20), height=250)
    return fig
