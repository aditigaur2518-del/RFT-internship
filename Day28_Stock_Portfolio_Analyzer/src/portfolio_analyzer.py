import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_FILE = "data/stock_data.csv"
OUTPUT_DIR = "output"
CHART_DIR = "charts"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CHART_DIR, exist_ok=True)

df = pd.read_csv(DATA_FILE)

df["Date"] = pd.to_datetime(df["Date"])

df["Investment"] = df["Quantity"] * df["Buy_Price"]
df["Current_Value"] = df["Quantity"] * df["Current_Price"]

df["Profit_Loss"] = df["Current_Value"] - df["Investment"]

df["Return_Percentage"] = (
    df["Profit_Loss"] / df["Investment"]
) * 100

df["Daily_Return"] = df.groupby("Stock")["Current_Price"].pct_change() * 100

stock_summary = df.groupby(
    ["Stock", "Sector"]
).agg(
    Quantity=("Quantity", "last"),
    Investment=("Investment", "last"),
    Current_Value=("Current_Value", "last"),
    Profit_Loss=("Profit_Loss", "last"),
    Return_Percentage=("Return_Percentage", "last")
).reset_index()

total_investment = stock_summary["Investment"].sum()
total_current_value = stock_summary["Current_Value"].sum()
total_profit_loss = stock_summary["Profit_Loss"].sum()

overall_return = (
    total_profit_loss / total_investment
) * 100

best_stock = stock_summary.loc[
    stock_summary["Return_Percentage"].idxmax()
]

worst_stock = stock_summary.loc[
    stock_summary["Return_Percentage"].idxmin()
]

print("\n" + "=" * 60)
print("        STOCK MARKET PORTFOLIO ANALYZER")
print("=" * 60)

print("\nSTOCK PERFORMANCE")
print("-" * 60)

print(
    stock_summary[
        [
            "Stock",
            "Sector",
            "Investment",
            "Current_Value",
            "Profit_Loss",
            "Return_Percentage"
        ]
    ].to_string(index=False)
)

print("\n" + "-" * 60)
print("PORTFOLIO SUMMARY")
print("-" * 60)

print(f"Total Investment : ₹{total_investment:,.2f}")
print(f"Current Value    : ₹{total_current_value:,.2f}")
print(f"Total Profit/Loss: ₹{total_profit_loss:,.2f}")
print(f"Overall Return   : {overall_return:.2f}%")

print("\nBEST PERFORMING STOCK")
print(f"Stock  : {best_stock['Stock']}")
print(f"Return : {best_stock['Return_Percentage']:.2f}%")

print("\nWORST PERFORMING STOCK")
print(f"Stock  : {worst_stock['Stock']}")
print(f"Return : {worst_stock['Return_Percentage']:.2f}%")

# Portfolio Growth Chart

portfolio_growth = df.groupby("Date").agg(
    Investment=("Investment", "sum"),
    Current_Value=("Current_Value", "sum")
).reset_index()

plt.figure(figsize=(10, 6))

plt.plot(
    portfolio_growth["Date"],
    portfolio_growth["Current_Value"],
    marker="o",
    label="Portfolio Value"
)

plt.plot(
    portfolio_growth["Date"],
    portfolio_growth["Investment"],
    linestyle="--",
    label="Investment"
)

plt.title("Portfolio Growth")
plt.xlabel("Date")
plt.ylabel("Value (₹)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "portfolio_growth.png")
)

plt.close()

# Sector-wise Investment Chart

sector_investment = stock_summary.groupby(
    "Sector"
)["Investment"].sum()

plt.figure(figsize=(8, 6))

sector_investment.plot(
    kind="bar"
)

plt.title("Sector-wise Investment")
plt.xlabel("Sector")
plt.ylabel("Investment (₹)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "sector_investment.png")
)

plt.close()

# Daily Return Analysis

daily_returns = df.groupby("Date")[
    "Daily_Return"
].mean()

plt.figure(figsize=(10, 6))

daily_returns.plot(
    kind="line",
    marker="o"
)

plt.axhline(
    0,
    linestyle="--"
)

plt.title("Daily Return Analysis")
plt.xlabel("Date")
plt.ylabel("Daily Return (%)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "daily_returns.png")
)

plt.close()

# Moving Average Prediction

moving_average = df.groupby("Date")[
    "Current_Price"
].mean()

moving_average_3 = moving_average.rolling(
    window=3
).mean()

last_ma = moving_average_3.iloc[-1]
last_price = moving_average.iloc[-1]

print("\nMOVING AVERAGE PREDICTION")
print("-" * 60)

if last_price > last_ma:
    trend = "UPWARD"
elif last_price < last_ma:
    trend = "DOWNWARD"
else:
    trend = "SIDEWAYS"

print(f"Latest Average Price : ₹{last_price:.2f}")
print(f"3-Day Moving Average : ₹{last_ma:.2f}")
print(f"Predicted Trend      : {trend}")

# Export Report

stock_summary.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "portfolio_report.csv"
    ),
    index=False
)

print("\nReport exported to:")
print("output/portfolio_report.csv")

print("\nCharts generated:")
print("charts/portfolio_growth.png")
print("charts/sector_investment.png")
print("charts/daily_returns.png")

print("\nAnalysis completed successfully!")