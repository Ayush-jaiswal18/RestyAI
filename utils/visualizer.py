import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_sleep_duration_trend(df):
    """Create a line plot showing sleep duration trend."""
    fig = go.Figure()
    
    # Add actual duration line
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['duration'],
        name='Sleep Duration',
        line=dict(color='#1f77b4'),
        mode='lines+markers'
    ))
    
    # Add rolling average line
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['rolling_avg_duration'],
        name='7-day Average',
        line=dict(color='#ff7f0e', dash='dash'),
        mode='lines'
    ))
    
    fig.update_layout(
        title='Sleep Duration Over Time',
        xaxis_title='Date',
        yaxis_title='Hours of Sleep',
        hovermode='x unified',
        showlegend=True
    )
    
    return fig

def plot_sleep_quality_heatmap(df):
    """Create a heatmap of sleep quality by day and hour."""
    # Pivot data for heatmap
    pivot_df = df.pivot_table(
        values='quality',
        index=df['sleep_start'].dt.hour,
        columns=df['day_of_week'],
        aggfunc='mean'
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        colorscale='RdYlBu',
        zmin=0,
        zmax=100
    ))
    
    fig.update_layout(
        title='Sleep Quality by Day and Hour',
        xaxis_title='Day of Week',
        yaxis_title='Hour of Day'
    )
    
    return fig

def plot_weekly_sleep_cycle(df):
    """Create a box plot showing sleep patterns by day of week."""
    fig = go.Figure()
    
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    fig.add_trace(go.Box(
        x=df['day_of_week'],
        y=df['duration'],
        name='Sleep Duration',
        boxpoints='outliers',
        marker_color='#1f77b4'
    ))
    
    fig.update_layout(
        title='Weekly Sleep Pattern Distribution',
        xaxis=dict(
            title='Day of Week',
            categoryorder='array',
            categoryarray=days_order
        ),
        yaxis=dict(
            title='Hours of Sleep'
        )
    )
    
    return fig
