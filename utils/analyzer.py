import pandas as pd
import numpy as np
from scipy import stats

def calculate_sleep_metrics(df):
    """Calculate key sleep metrics."""
    metrics = {
        'avg_duration': df['duration'].mean(),
        'efficiency': (df['duration'].mean() / 8) * 100,  # Assuming 8 hours is ideal
        'avg_latency': df['latency'].mean(),
        'quality_score': df['quality'].mean(),
        'consistency': 100 - df['duration'].std() * 10  # Higher consistency = lower std dev
    }

    return metrics

def perform_statistical_analysis(df):
    """Perform detailed statistical analysis on sleep data."""
    analysis = {
        'Sleep Duration': {
            'Summary Statistics': {
                'Average Sleep': f"{df['duration'].mean():.2f} hours",
                'Median Sleep': f"{df['duration'].median():.2f} hours",
                'Standard Deviation': f"{df['duration'].std():.2f} hours",
                'Minimum': f"{df['duration'].min():.2f} hours",
                'Maximum': f"{df['duration'].max():.2f} hours",
                'Range': f"{df['duration'].max() - df['duration'].min():.2f} hours"
            },
            'Distribution Analysis': {
                'Skewness': f"{stats.skew(df['duration']):.2f}",
                'Kurtosis': f"{stats.kurtosis(df['duration']):.2f}",
                'Is Normal Distribution': 'Yes' if stats.normaltest(df['duration'])[1] > 0.05 else 'No'
            }
        },
        'Sleep Quality': {
            'Summary Statistics': {
                'Average Quality': f"{df['quality'].mean():.1f}/100",
                'Median Quality': f"{df['quality'].median():.1f}/100",
                'Quality Variation': f"{df['quality'].std():.1f}",
                'Best Quality': f"{df['quality'].max():.1f}/100",
                'Lowest Quality': f"{df['quality'].min():.1f}/100"
            },
            'Quality Distribution': {
                'Excellent (90-100)': f"{len(df[df['quality'] >= 90])} nights",
                'Good (80-89)': f"{len(df[(df['quality'] >= 80) & (df['quality'] < 90)])} nights",
                'Fair (70-79)': f"{len(df[(df['quality'] >= 70) & (df['quality'] < 80)])} nights",
                'Poor (<70)': f"{len(df[df['quality'] < 70])} nights"
            }
        },
        'Sleep Patterns': {
            'Timing Analysis': {
                'Average Bedtime': f"{df['sleep_start'].dt.hour.mean():.1f}:00",
                'Most Common Bedtime': f"{df['sleep_start'].dt.hour.mode()[0]}:00",
                'Average Wake Time': f"{df['sleep_end'].dt.hour.mean():.1f}:00",
                'Sleep Schedule Consistency': f"{100 - df['sleep_start'].dt.hour.std() * 10:.1f}%"
            },
            'Weekly Patterns': {
                'Best Sleep Day': df.groupby('day_of_week')['quality'].mean().idxmax(),
                'Longest Sleep Day': df.groupby('day_of_week')['duration'].mean().idxmax(),
                'Most Consistent Day': df.groupby('day_of_week')['duration'].std().idxmin()
            }
        },
        'Correlations': {
            'Duration vs Quality': f"{df['duration'].corr(df['quality']):.2f}",
            'Interpretation': {
                'Sleep Duration': get_duration_interpretation(df['duration'].mean()),
                'Sleep Quality': get_quality_interpretation(df['quality'].mean()),
                'Schedule Consistency': get_consistency_interpretation(df['sleep_start'].dt.hour.std())
            }
        }
    }

    return analysis

def get_duration_interpretation(avg_duration):
    """Get interpretation of sleep duration."""
    if avg_duration >= 8:
        return "Optimal sleep duration achieved"
    elif avg_duration >= 7:
        return "Good sleep duration, but could be improved"
    elif avg_duration >= 6:
        return "Below recommended sleep duration"
    else:
        return "Significantly below recommended sleep duration"

def get_quality_interpretation(avg_quality):
    """Get interpretation of sleep quality."""
    if avg_quality >= 90:
        return "Excellent sleep quality"
    elif avg_quality >= 80:
        return "Good sleep quality"
    elif avg_quality >= 70:
        return "Fair sleep quality"
    else:
        return "Poor sleep quality, improvement needed"

def get_consistency_interpretation(time_std):
    """Get interpretation of sleep schedule consistency."""
    if time_std < 0.5:
        return "Very consistent sleep schedule"
    elif time_std < 1:
        return "Moderately consistent sleep schedule"
    elif time_std < 1.5:
        return "Somewhat inconsistent sleep schedule"
    else:
        return "Highly irregular sleep schedule"