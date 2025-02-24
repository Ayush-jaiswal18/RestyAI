import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew, kurtosis, normaltest

# Load the data
data = pd.read_csv('assets/sample_data.csv', parse_dates=['sleep_start', 'sleep_end'])

# Calculate sleep duration in hours
data['sleep_duration'] = (data['sleep_end'] - data['sleep_start']).dt.total_seconds() / 3600

# Summary statistics
summary_stats = data['sleep_duration'].describe()
skewness = skew(data['sleep_duration'])
kurt = kurtosis(data['sleep_duration'])
normal_test = normaltest(data['sleep_duration'])
is_normal = 'Yes' if normal_test.pvalue > 0.05 else 'No'

# Print summary statistics
print("Summary Statistics:")
print(summary_stats)
print(f"Skewness: {skewness:.2f}")
print(f"Kurtosis: {kurt:.2f}")
print(f"Is Normal Distribution: {is_normal}")

# Plot sleep duration distribution
plt.figure(figsize=(10, 6))
sns.histplot(data['sleep_duration'], kde=True)
plt.title('Sleep Duration Distribution')
plt.xlabel('Sleep Duration (hours)')
plt.ylabel('Frequency')
plt.savefig('sleep_duration_distribution.png')
plt.show()

# Create a table for summary statistics
summary_table = pd.DataFrame({
    'Statistic': ['Mean', 'Standard Deviation', 'Min', '25%', '50%', '75%', 'Max', 'Skewness', 'Kurtosis', 'Is Normal Distribution'],
    'Value': [summary_stats['mean'], summary_stats['std'], summary_stats['min'], summary_stats['25%'], summary_stats['50%'], summary_stats['75%'], summary_stats['max'], skewness, kurt, is_normal]
})

# Save the summary table to a CSV file
summary_table.to_csv('summary_statistics.csv', index=False)
