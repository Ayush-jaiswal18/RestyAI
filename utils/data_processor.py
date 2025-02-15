import pandas as pd
from datetime import datetime, timedelta

def validate_data(df):
    """Validate the input dataframe structure and data types."""
    required_columns = ['date', 'sleep_start', 'sleep_end', 'quality']
    
    # Check for required columns
    if not all(col in df.columns for col in required_columns):
        raise ValueError("Missing required columns. Please ensure your CSV contains: date, sleep_start, sleep_end, quality")
    
    # Convert date columns
    df['date'] = pd.to_datetime(df['date'])
    df['sleep_start'] = pd.to_datetime(df['sleep_start'])
    df['sleep_end'] = pd.to_datetime(df['sleep_end'])
    
    # Validate quality scores
    if not df['quality'].between(0, 100).all():
        raise ValueError("Sleep quality scores must be between 0 and 100")
    
    return True

def process_sleep_data(df):
    """Process the raw sleep data and calculate additional metrics."""
    # Create a copy to avoid modifying original data
    processed_df = df.copy()
    
    # Convert datetime columns
    processed_df['date'] = pd.to_datetime(processed_df['date'])
    processed_df['sleep_start'] = pd.to_datetime(processed_df['sleep_start'])
    processed_df['sleep_end'] = pd.to_datetime(processed_df['sleep_end'])
    
    # Calculate sleep duration
    processed_df['duration'] = (processed_df['sleep_end'] - processed_df['sleep_start']).dt.total_seconds() / 3600
    
    # Calculate sleep latency (assuming ideal bedtime is 22:00)
    ideal_bedtime = processed_df['date'].dt.normalize() + pd.Timedelta(hours=22)
    processed_df['latency'] = (processed_df['sleep_start'] - ideal_bedtime).dt.total_seconds() / 60
    
    # Extract day of week
    processed_df['day_of_week'] = processed_df['date'].dt.day_name()
    
    # Calculate rolling averages
    processed_df['rolling_avg_duration'] = processed_df['duration'].rolling(window=7, min_periods=1).mean()
    processed_df['rolling_avg_quality'] = processed_df['quality'].rolling(window=7, min_periods=1).mean()
    
    return processed_df