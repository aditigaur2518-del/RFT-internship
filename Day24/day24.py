import pandas as pd
import matplotlib.pyplot as plt

file_name = "weather_data.csv"

df = pd.read_csv(file_name)

df["Date"] = pd.to_datetime(df["Date"])
df["Temperature"] = pd.to_numeric(df["Temperature"], errors="coerce")

df = df.dropna()
df = df.drop_duplicates()

print("\n========== WEATHER DATA ==========\n")
print(df)

average_temperature = df.groupby("City")["Temperature"].mean().sort_values(ascending=False)

print("\n========== AVERAGE TEMPERATURE ==========\n")
print(average_temperature.round(2))

hottest_city = average_temperature.idxmax()
hottest_temperature = average_temperature.max()

coldest_city = average_temperature.idxmin()
coldest_temperature = average_temperature.min()

print("\n========== HOTTEST CITY ==========")
print(f"{hottest_city}: {hottest_temperature:.2f}°C")

print("\n========== COLDEST CITY ==========")
print(f"{coldest_city}: {coldest_temperature:.2f}°C")

rainy_days = (df["Weather"].str.lower() == "rainy").sum()
sunny_days = (df["Weather"].str.lower() == "sunny").sum()

print("\n========== WEATHER SUMMARY ==========")
print(f"Rainy Days: {rainy_days}")
print(f"Sunny Days: {sunny_days}")

weather_distribution = df["Weather"].value_counts()

print("\n========== WEATHER DISTRIBUTION ==========")
print(weather_distribution)

daily_temperature = df.groupby("Date")["Temperature"].mean()

plt.figure(figsize=(10, 5))
plt.plot(
    daily_temperature.index,
    daily_temperature.values,
    marker="o"
)
plt.title("Temperature Trend")
plt.xlabel("Date")
plt.ylabel("Average Temperature (°C)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("temperature_trend.png")
plt.show()

plt.figure(figsize=(7, 5))
plt.bar(
    weather_distribution.index,
    weather_distribution.values
)
plt.title("Weather Distribution")
plt.xlabel("Weather")
plt.ylabel("Number of Days")
plt.tight_layout()
plt.savefig("weather_distribution.png")
plt.show()

plt.figure(figsize=(8, 5))
plt.bar(
    average_temperature.index,
    average_temperature.values
)
plt.title("Average Temperature per City")
plt.xlabel("City")
plt.ylabel("Average Temperature (°C)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("average_temperature_city.png")
plt.show()

report = average_temperature.reset_index()
report.columns = ["City", "Average Temperature"]

report["Hottest City"] = hottest_city
report["Coldest City"] = coldest_city
report["Rainy Days"] = rainy_days
report["Sunny Days"] = sunny_days

report.to_csv("weather_final_report.csv", index=False)

print("\nFinal report exported successfully!")
print("File: weather_final_report.csv")

#################################################

window = 3

temperature_series = df.groupby("Date")["Temperature"].mean()

moving_average = temperature_series.rolling(window=window).mean()

predicted_temperature = moving_average.iloc[-1]

print("\n========== TOMORROW'S TEMPERATURE PREDICTION ==========")
print(f"Predicted Temperature: {predicted_temperature:.2f}°C")

prediction_report = pd.DataFrame({
    "Date": ["Tomorrow"],
    "Predicted Temperature": [round(predicted_temperature, 2)]
})

prediction_report.to_csv(
    "tomorrow_temperature_prediction.csv",
    index=False
)

print("Prediction exported successfully!")
