import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# Custom CSS for modern UI
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1a1f35 0%, #2d3250 100%);
        color: #ffffff;
    }
    
    .main-title {
        font-size: 2.5em;
        background: linear-gradient(45deg, #00d4ff, #00ffa3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1em;
    }
    
    .card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .metric-card {
        background: rgba(0, 212, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    
    .chart-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Main Dashboard Layout
st.markdown('<h1 class="main-title">AI Workforce Analytics Dashboard</h1>', unsafe_allow_html=True)

# Create main dashboard tabs
tabs = st.tabs(["Analytics Dashboard", "Workforce Optimization", "Team Insights", "Settings"])

with tabs[0]:
    # Analytics Dashboard
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Efficiency Score", "94%", "+5%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Current Staff", "45", "-2")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Productivity", "87%", "+3%")
        st.markdown('</div>', unsafe_allow_html=True)

    # Staffing Heatmap
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📊 Staffing Heatmap")
    
    # Generate sample heatmap data
    hours = list(range(24))
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    staffing_data = np.random.randint(70, 100, size=(7, 24))
    
    fig = go.Figure(data=go.Heatmap(
        z=staffing_data,
        x=hours,
        y=days,
        colorscale='RdYlGn',
        hoverongaps=False))
    
    fig.update_layout(
        title="Weekly Staffing Levels",
        xaxis_title="Hour of Day",
        yaxis_title="Day of Week",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # AI Insights
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🤖 AI-Powered Insights")
    
    insights = [
        "⚠️ Potential understaffing detected for next Monday morning",
        "💡 Recommended: Adjust break schedules to optimize coverage",
        "📈 Team productivity increased by 12% this week",
        "🎯 Suggested: Cross-train 3 employees for better flexibility"
    ]
    
    for insight in insights:
        st.info(insight)
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[1]:
    # Workforce Optimization
    st.subheader("Smart Scheduling")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_date = st.date_input(
            "Select Date",
            min_value=datetime.now().date(),
            max_value=datetime.now().date() + timedelta(days=30)
        )
    
    with col2:
        department = st.selectbox(
            "Select Department",
            ["Sales", "Support", "Operations", "Technical"]
        )
    
    if st.button("Generate Optimal Schedule"):
        with st.spinner("AI generating optimal schedule..."):
            # Simulated schedule generation
            st.success("✅ Schedule generated successfully!")
            
            # Create time range for a workday
            time_range = pd.date_range(
                start=f"{selected_date} 09:00:00",
                end=f"{selected_date} 17:00:00",
                freq="H"
            )
            
            # Create sample data with matching lengths
            n_hours = len(time_range)
            schedule_data = pd.DataFrame({
                'Time': time_range,
                'Required Staff': np.random.randint(5, 15, size=n_hours),
                'Scheduled Staff': np.random.randint(5, 15, size=n_hours)
            })
            
            # Display the schedule
            st.line_chart(schedule_data.set_index('Time'))
            
            # Show detailed schedule
            st.dataframe(schedule_data.set_index('Time'))

with tabs[2]:
    # Team Insights
    st.subheader("Team Performance Analytics")
    
    # Performance metrics
    performance_data = pd.DataFrame({
        'Metric': ['Task Completion', 'Customer Satisfaction', 'Response Time', 'Quality Score'],
        'Score': [87, 92, 85, 90]
    })
    
    fig = px.bar(performance_data, x='Metric', y='Score',
                 color='Score',
                 color_continuous_scale='Viridis',
                 title='Team Performance Metrics')
    
    st.plotly_chart(fig, use_container_width=True)

with tabs[3]:
    # Settings
    st.subheader("Dashboard Settings")
    
    st.toggle("Enable AI Notifications")
    st.toggle("Dark Mode")
    st.select_slider("Update Frequency", options=['1h', '2h', '4h', '8h'])
    
    with st.expander("Export Options"):
        st.download_button(
            "Export Analytics Report",
            data="sample_data",
            file_name="analytics_report.csv",
            mime="text/csv"
        )

# Footer
st.markdown("""
    <div style='text-align: center; color: #888; padding: 20px; font-size: 0.8em;'>
        Powered by Advanced AI Analytics | Version 2.0
    </div>
""", unsafe_allow_html=True)
