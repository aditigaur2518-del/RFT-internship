import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dates = pd.date_range(start="2026-01-01", periods=20)

prices = [100, 102, 101, 105, 107, 110, 108, 111, 115, 117,
          114, 118, 120, 119, 123, 125, 122, 128, 130, 127]

df = pd.DataFrame({
    "Date": dates,
    "Stock_Price": prices
})

df["MA_5"] = df["Stock_Price"].rolling(window=5).mean()

df["Daily_Return"] = df["Stock_Price"].pct_change()

volatility = df["Daily_Return"].std()

peak_index = df["Stock_Price"].idxmax()
drop_index = df["Stock_Price"].idxmin()

peak_price = df.loc[peak_index, "Stock_Price"]
drop_price = df.loc[drop_index, "Stock_Price"]

peak_date = df.loc[peak_index, "Date"]
drop_date = df.loc[drop_index, "Date"]

print("\n========= STOCK ANALYSIS REPORT =========")
print(f"Highest Price : {peak_price} on {peak_date.date()}")
print(f"Lowest Price  : {drop_price} on {drop_date.date()}")
print(f"Volatility    : {round(volatility, 4)}")
print("=========================================\n")

plt.figure(figsize=(14, 7))

plt.plot(
    df["Date"],
    df["Stock_Price"],
    marker='o',
    linewidth=2,
    label="Stock Price"
)

plt.plot(
    df["Date"],
    df["MA_5"],
    linestyle='--',
    linewidth=3,
    label="5-Day Moving Average"
)

plt.scatter(
    peak_date,
    peak_price,
    s=200,
    marker='^',
    label="Peak Price"
)

plt.scatter(
    drop_date,
    drop_price,
    s=200,
    marker='v',
    label="Lowest Price"
)

plt.fill_between(
    df["Date"],
    df["Stock_Price"],
    alpha=0.2
)

plt.title("Stock Market Time-Series Analysis", fontsize=18)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Stock Price", fontsize=12)

plt.xticks(rotation=45)

plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()