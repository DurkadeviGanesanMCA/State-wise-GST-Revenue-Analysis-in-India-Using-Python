import pandas as pd
import numpy as np

def load_and_filter_data(file_path, selected_years, selected_states):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    
    # Filter by Year
    if selected_years:
        df = df[df['Year'].isin(selected_years)]
        
    # Filter by State
    if selected_states and "All" not in selected_states:
        df = df[df['State Name'].isin(selected_states)]
        
    return df

def calculate_kpis(df):
    if df.empty:
        return {"total_gst": 0, "avg_gst": 0, "top_state": "N/A", "top_val": 0, "bottom_state": "N/A", "bottom_val": 0}
        
    total_gst = df['Total_GST'].sum()
    
    # Average monthly systemic collection
    avg_gst = df.groupby(['Year', 'Month'])['Total_GST'].sum().mean()
    if np.isnan(avg_gst): avg_gst = 0
        
    # State Rankings
    state_totals = df.groupby('State Name')['Total_GST'].sum()
    top_state = state_totals.idxmax() if not state_totals.empty else "N/A"
    top_val = state_totals.max() if not state_totals.empty else 0
    
    bottom_state = state_totals.idxmin() if not state_totals.empty else "N/A"
    bottom_val = state_totals.min() if not state_totals.empty else 0
    
    return {
        "total_gst": total_gst,
        "avg_gst": avg_gst,
        "top_state": top_state,
        "top_val": top_val,
        "bottom_state": bottom_state,
        "bottom_val": bottom_val
    }
