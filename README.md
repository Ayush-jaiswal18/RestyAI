# RestyAI

## Overview
RestyAI is a Streamlit-based web application designed to help users analyze their sleep patterns and gain insights into their sleep quality. By uploading a CSV file containing sleep data, users can visualize trends, calculate sleep metrics, and detect potential sleep disorders.

## Features
- **CSV File Upload**: Upload your sleep data in CSV format.
- **Data Validation**: Ensure the uploaded data meets the required format.
- **Sleep Metrics Calculation**: Calculate average sleep duration, sleep efficiency, and average time to sleep.
- **Visualizations**: 
  - Sleep duration trend
  - Weekly sleep patterns
  - Sleep quality heatmap
  - Sleep quality distribution pie chart
  - Sleep duration gauge chart
  - Weekly sleep patterns bar chart
  - Sleep quality bullet chart
  - Timing analysis bar chart
- **Statistical Analysis**: Perform statistical analysis on sleep data.
- **Sleep Disorder Detection**: Detect potential sleep disorders and provide recommendations.
- **Export Functionality**: Download the processed sleep data.

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/Ayush-jaiswal18/RestyAI.git
    ```
2. Navigate to the project directory:
    ```sh
    cd sleep-pattern-analyzer
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Run the Streamlit application:
    ```sh
    streamlit run main.py
    ```
2. Open your web browser and go to `http://localhost:8501`.
3. Upload your sleep data CSV file and explore the analysis and visualizations.

## CSV File Format
Your CSV file should have the following columns:
- **date**: The date of sleep (YYYY-MM-DD)
- **sleep_start**: Start time of sleep (YYYY-MM-DD HH:MM:SS)
- **sleep_end**: End time of sleep (YYYY-MM-DD HH:MM:SS)
- **quality**: Sleep quality score (0-100)

## Sample Data
Here is a sample of the expected CSV format:
```csv
date,sleep_start,sleep_end,quality
2023-01-01,2023-01-01 23:00:00,2023-01-02 07:00:00,85
2023-01-02,2023-01-02 23:30:00,2023-01-03 07:30:00,78
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
