import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_processor import process_sleep_data, validate_data
from utils.visualizer import (
    plot_sleep_duration_trend,
    plot_sleep_quality_heatmap,
    plot_weekly_sleep_cycle
)
from utils.analyzer import calculate_sleep_metrics, perform_statistical_analysis
from utils.disorder_detector import SleepDisorderDetector

st.set_page_config(
    page_title="Sleep Pattern Analyzer",
    page_icon="🌙",
    layout="wide"
)

# Sample data format
sample_data = """date,sleep_start,sleep_end,quality
2023-01-01,2023-01-01 23:00:00,2023-01-02 07:00:00,85
2023-01-02,2023-01-02 23:30:00,2023-01-03 07:30:00,78"""

def main():
    st.title("🌙 Sleep Pattern Analyzer")
    st.write("Upload your sleep data to analyze patterns and get insights")

    # Show CSV format instructions
    with st.expander("📝 CSV File Format Instructions"):
        st.write("""
        Your CSV file should have the following columns:
        1. **date**: The date of sleep (YYYY-MM-DD)
        2. **sleep_start**: Start time of sleep (YYYY-MM-DD HH:MM:SS)
        3. **sleep_end**: End time of sleep (YYYY-MM-DD HH:MM:SS)
        4. **quality**: Sleep quality score (0-100)
        """)
        st.code(sample_data, language="csv")

        # Add download sample data button
        st.download_button(
            label="Download Sample CSV",
            data=sample_data,
            file_name="sample_sleep_data.csv",
            mime="text/csv"
        )

    # File upload
    uploaded_file = st.file_uploader(
        "Upload your sleep data CSV file",
        type=['csv'],
        help="Upload a CSV file with columns: date, sleep_start, sleep_end, quality"
    )

    if uploaded_file is not None:
        try:
            # Read and validate data
            df = pd.read_csv(uploaded_file)
            if validate_data(df):
                # Process data
                processed_df = process_sleep_data(df)

                # Calculate metrics
                metrics = calculate_sleep_metrics(processed_df)

                # Display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Average Sleep Duration", f"{metrics['avg_duration']:.1f}h")
                with col2:
                    st.metric("Sleep Efficiency", f"{metrics['efficiency']:.1f}%")
                with col3:
                    st.metric("Average Time to Sleep", f"{metrics['avg_latency']:.0f}min")

                # Visualizations
                st.subheader("Sleep Duration Trend")
                fig_duration = plot_sleep_duration_trend(processed_df)
                st.plotly_chart(fig_duration, use_container_width=True, key="duration_trend")

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Weekly Sleep Pattern")
                    fig_weekly = plot_weekly_sleep_cycle(processed_df)
                    st.plotly_chart(fig_weekly, use_container_width=True, key="weekly_pattern")

                with col2:
                    st.subheader("Sleep Quality Heatmap")
                    fig_quality = plot_sleep_quality_heatmap(processed_df)
                    st.plotly_chart(fig_quality, use_container_width=True, key="quality_heatmap")

                # Statistical Analysis
                st.header("📊 Statistical Analysis")
                stats = perform_statistical_analysis(processed_df)

                # Sleep Quality Distribution Pie Chart
                quality_dist = stats['Sleep Quality']['Quality Distribution']
                quality_data = {k: int(v.split()[0]) for k, v in quality_dist.items()}

                fig_quality_dist = px.pie(
                    values=list(quality_data.values()),
                    names=list(quality_data.keys()),
                    title="Sleep Quality Distribution",
                    color_discrete_sequence=px.colors.sequential.RdBu
                )
                st.plotly_chart(fig_quality_dist, key="quality_distribution")

                # Sleep Duration Analysis
                with st.expander("🕒 Sleep Duration Analysis", expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("📈 Summary Statistics")
                        duration_stats = stats['Sleep Duration']['Summary Statistics']

                        # Create gauge chart for average sleep
                        avg_sleep = float(duration_stats['Average Sleep'].split()[0])
                        fig_gauge = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=avg_sleep,
                            title={'text': "Average Sleep Duration"},
                            domain={'x': [0, 1], 'y': [0, 1]},
                            gauge={
                                'axis': {'range': [0, 12]},
                                'steps': [
                                    {'range': [0, 6], 'color': "lightgray"},
                                    {'range': [6, 7], 'color': "gray"},
                                    {'range': [7, 9], 'color': "lightgreen"},
                                    {'range': [9, 12], 'color': "gray"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 8
                                }
                            }
                        ))
                        st.plotly_chart(fig_gauge, key="gauge_chart")

                    with col2:
                        st.write("📉 Distribution Analysis")
                        st.json(stats['Sleep Duration']['Distribution Analysis'])

                # Weekly Sleep Patterns Bar Chart
                weekly_patterns = stats['Sleep Patterns']['Weekly Patterns']
                day_quality = processed_df.groupby('day_of_week')['quality'].mean().round(2)
                day_duration = processed_df.groupby('day_of_week')['duration'].mean().round(2)

                fig_weekly = go.Figure()
                fig_weekly.add_trace(go.Bar(
                    x=day_quality.index,
                    y=day_quality.values,
                    name='Quality Score',
                    marker_color='rgb(55, 83, 109)'
                ))
                fig_weekly.add_trace(go.Bar(
                    x=day_duration.index,
                    y=day_duration.values,
                    name='Duration (hours)',
                    marker_color='rgb(26, 118, 255)'
                ))

                fig_weekly.update_layout(
                    title='Weekly Sleep Patterns',
                    xaxis_tickfont_size=14,
                    yaxis=dict(
                        title='Score / Hours',
                        title_font=dict(size=16),
                        tickfont_size=14,
                    ),
                    barmode='group'
                )
                st.plotly_chart(fig_weekly, use_container_width=True, key="weekly_patterns_1")
                st.plotly_chart(fig_weekly, use_container_width=True, key="weekly_patterns_2")

                # Sleep Quality Analysis with Bullet Charts
                with st.expander("💤 Sleep Quality Analysis", expanded=True):
                    quality_stats = stats['Sleep Quality']['Summary Statistics']
                    avg_quality = float(quality_stats['Average Quality'].split('/')[0])

                    fig_bullet = go.Figure(go.Indicator(
                        mode = "number+gauge+delta",
                        value = avg_quality,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Sleep Quality Score"},
                        delta = {'reference': 85},
                        gauge = {
                            'axis': {'range': [0, 100]},
                            'steps': [
                                {'range': [0, 60], 'color': "lightgray"},
                                {'range': [60, 70], 'color': "gray"},
                                {'range': [70, 85], 'color': "lightblue"},
                                {'range': [85, 100], 'color': "blue"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 85
                            },
                            'bar': {'color': "darkblue"}
                        }
                    ))
                    st.plotly_chart(fig_bullet, key="bullet_chart")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("📊 Quality Statistics")
                        st.json(stats['Sleep Quality']['Summary Statistics'])
                    with col2:
                        st.write("🎯 Quality Distribution")
                        st.json(stats['Sleep Quality']['Quality Distribution'])

                # Sleep Patterns
                with st.expander("🔄 Sleep Patterns", expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("⏰ Timing Analysis")
                        st.json(stats['Sleep Patterns']['Timing Analysis'])
                    with col2:
                        st.write("📅 Weekly Patterns")
                        st.json(stats['Sleep Patterns']['Weekly Patterns'])

                # Correlations and Interpretations
                with st.expander("🔍 Analysis Insights", expanded=True):
                    st.write("📊 Correlations")
                    st.write(f"Duration vs Quality Correlation: {stats['Correlations']['Duration vs Quality']}")

                    st.write("💡 Interpretations")
                    interpretations = stats['Correlations']['Interpretation']
                    for key, value in interpretations.items():
                        st.info(f"**{key}**: {value}")

                # Add Sleep Disorder Analysis section
                st.header("🏥 Sleep Disorder Analysis")

                # Initialize detector
                detector = SleepDisorderDetector()
                disorder_analysis = detector.analyze_sleep_patterns(processed_df)

                # Display disorder analysis results
                if disorder_analysis['detected_disorders']:
                    st.warning("Potential sleep disorders detected. Please consult a healthcare professional for proper diagnosis.")

                    for disorder in disorder_analysis['detected_disorders']:
                        risk_info = disorder_analysis['risk_levels'][disorder]
                        with st.expander(f"📊 {disorder} Analysis", expanded=True):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric(
                                    "Risk Level",
                                    f"{risk_info['risk_level']*100:.1f}%",
                                    delta=None,
                                    delta_color="inverse"
                                )
                                st.metric(
                                    "Confidence Score",
                                    f"{risk_info['confidence']*100:.1f}%"
                                )

                            with col2:
                                st.write("📝 Evidence:")
                                for evidence in risk_info['evidence']:
                                    st.write(f"- {evidence}")

                    # Display recommendations
                    st.subheader("💡 Recommendations")
                    for i, recommendation in enumerate(disorder_analysis['recommendations'], 1):
                        st.info(f"{i}. {recommendation}")
                else:
                    st.success("No significant sleep disorders detected in the current data.")

                # Export functionality
                st.subheader("Export Analysis")
                csv = processed_df.to_csv(index=False)
                st.download_button(
                    label="Download Processed Data",
                    data=csv,
                    file_name="processed_sleep_data.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

    else:
        st.info("Please upload a CSV file to begin analysis")

if __name__ == "__main__":
    main()