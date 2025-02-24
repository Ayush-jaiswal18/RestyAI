import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import json

# Load the data
data = pd.read_csv('assets/sample_data.csv')

# Calculate skewness and kurtosis
skewness = data['quality'].skew()
kurtosis = data['quality'].kurtosis()

# Check for normal distribution
k2, p = stats.normaltest(data['quality'])
is_normal = p > 0.05

# Print the distribution analysis
distribution_analysis = {
    "Skewness": skewness,
    "Kurtosis": kurtosis,
    "Is Normal Distribution": is_normal
}
print(json.dumps(distribution_analysis, indent=4))

# Plot the data
plt.figure(figsize=(10, 6))
plt.hist(data['quality'], bins=15, edgecolor='black')
plt.title('Sleep Quality Distribution')
plt.xlabel('Quality')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
