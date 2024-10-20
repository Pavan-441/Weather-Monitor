import requests
import schedule
import time
import sqlite3
import matplotlib.pyplot as plt

API_KEY = '4673480781602dbca308f02252003d15'

# Connect to the SQLite database
conn = sqlite3.connect('weather_data.db')
cursor = conn.cursor()

# Create a table for storing daily weather summaries
cursor.execute('''
CREATE TABLE IF NOT EXISTS daily_summary (
    date TEXT PRIMARY KEY,
    average_temp REAL,
    max_temp REAL,
    min_temp REAL,
    dominant_condition TEXT
)''')
conn.commit()

TEMP_THRESHOLD = 35  # Example threshold

def fetch_weather_data():
    cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
    today = time.strftime("%Y-%m-%d")
    
    # Initialize aggregate variables
    total_temp = 0
    max_temp = float('-inf')
    min_temp = float('inf')
    condition_count = {}

    for city in cities:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        try:
            response = requests.get(url)
            data = response.json()
            print(data)  # Debugging line to check the full response
            temp_c = data['main']['temp']  # Temperature in Celsius
            condition = data['weather'][0]['description']  # Weather condition
            print(f"Processed weather data for {city}: Temp={temp_c:.2f}°C, Condition={condition.capitalize()}")

            # Aggregate calculations
            total_temp += temp_c
            max_temp = max(max_temp, temp_c)
            min_temp = min(min_temp, temp_c)
            condition_count[condition] = condition_count.get(condition, 0) + 1

            # Check for alert conditions
            if temp_c > TEMP_THRESHOLD:
                print(f"ALERT: {city} temperature exceeds threshold! Current Temp={temp_c:.2f}°C")

        except Exception as e:
            print(f"Error fetching data for {city}: {e}")

    # After processing all cities, store daily summary
    if len(cities) > 0:
        avg_temp = total_temp / len(cities)
        dominant_condition = max(condition_count, key=condition_count.get)  # Get the dominant condition
        store_daily_summary(today, avg_temp, max_temp, min_temp, dominant_condition)

def store_daily_summary(date, avg_temp, max_temp, min_temp, dominant_condition):
    cursor.execute('SELECT * FROM daily_summary WHERE date = ?', (date,))
    row = cursor.fetchone()

    if row is None:
        cursor.execute('''
        INSERT INTO daily_summary (date, average_temp, max_temp, min_temp, dominant_condition) 
        VALUES (?, ?, ?, ?, ?)''', (date, avg_temp, max_temp, min_temp, dominant_condition))
    else:
        cursor.execute('''
        UPDATE daily_summary 
        SET average_temp = ?, max_temp = ?, min_temp = ?, dominant_condition = ?
        WHERE date = ?''', (avg_temp, max_temp, min_temp, dominant_condition, date))
    
    conn.commit()

def plot_weather_summary():
    cursor.execute('SELECT * FROM daily_summary')
    rows = cursor.fetchall()

    dates = [row[0] for row in rows]
    avg_temps = [row[1] for row in rows]
    max_temps = [row[2] for row in rows]
    min_temps = [row[3] for row in rows]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, avg_temps, label='Average Temp', color='blue')
    plt.plot(dates, max_temps, label='Max Temp', color='red')
    plt.plot(dates, min_temps, label='Min Temp', color='green')
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title('Daily Weather Summary')
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    print("Starting Weather Monitoring System...")
    schedule.every(5).minutes.do(fetch_weather_data)
    
    # Optional: schedule daily summary plotting
    schedule.every().day.at("18:00").do(plot_weather_summary)  # Example time for plotting

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()

# Close database connection
conn.close()
