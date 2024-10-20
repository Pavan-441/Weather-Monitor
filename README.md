# Weather Monitoring System

## Overview

The Weather Monitoring System is a Python-based application that fetches real-time weather data for multiple cities in India using the OpenWeatherMap API. It stores daily weather summaries in an SQLite database and provides visualizations of temperature trends over time.

## Features

- Fetches weather data for multiple cities.
- Stores daily weather summaries in an SQLite database.
- Alerts for temperature thresholds.
- Plots daily temperature trends using Matplotlib.
- Scheduled data fetching and plotting.

## Requirements

- Python 3.x
- Libraries:
  - `requests`
  - `schedule`
  - `sqlite3` (built-in)
  - `matplotlib`

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required libraries:
   ```bash
   pip install requests schedule matplotlib
   ```

3. Obtain an API key from OpenWeatherMap and replace the placeholder in the code:
   ```python
   API_KEY = 'your_api_key_here'
   ```

## Usage

1. Run the application:
   ```bash
   python weather_monitoring_system.py
   ```

2. The system will fetch weather data every 5 minutes and print the results in the console.

3. Daily summaries will be stored in the SQLite database `weather_data.db`.

4. A plot of the daily temperature summary will be generated at 6:00 PM each day.

## Code Explanation

- **fetch_weather_data()**: 
  - Fetches weather data for specified cities and calculates average, max, and min temperatures.
  - Checks for temperatures exceeding the defined threshold and alerts the user.

- **store_daily_summary(date, avg_temp, max_temp, min_temp, dominant_condition)**: 
  - Stores or updates the daily weather summary in the SQLite database.

- **plot_weather_summary()**: 
  - Retrieves stored data from the database and generates a plot of average, max, and min temperatures.

- **main()**: 
  - Initializes the weather monitoring system, scheduling tasks for data fetching and plotting.

## Example Output

The following output shows the processed weather data for various cities:
```
Starting Weather Monitoring System...
Processed weather data for Delhi: Temp=27.05°C, Condition=Haze
Processed weather data for Mumbai: Temp=29.99°C, Condition=Haze
Processed weather data for Chennai: Temp=28.26°C, Condition=Overcast clouds
Processed weather data for Bangalore: Temp=23.01°C, Condition=Scattered clouds
Processed weather data for Kolkata: Temp=26.97°C, Condition=Haze
Processed weather data for Hyderabad: Temp=26.23°C, Condition=Haze
```

## Contributing

Feel free to fork the repository and submit pull requests for any improvements or features you'd like to add!

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any inquiries or issues, please contact:
- Email: pavank0066@gmail.com

---
