import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Stock Portfolio Analyzer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock Market Portfolio Analyzer")

st.write(
    "Analyze stock performance, portfolio returns, "
    "sector investments and daily returns."
)

df = pd.read_csv("data/stock_data.csv")

df["Date"] = pd.to_datetime(df["Date"])

df["Investment"] = (
    df["Quantity"] * df["Buy_Price"]
)

df["Current_Value"] = (
    df["Quantity"] * df["Current_Price"]
)

df["Profit_Loss"] = (
    df["Current_Value"] - df["Investment"]
)

df["Return_Percentage"] = (
    df["Profit_Loss"] / df["Investment"]
) * 100

df["Daily_Return"] = (
    df.groupby("Stock")["Current_Price"]
    .pct_change()
    * 100
)

# Sidebar

st.sidebar.header("Filters")

stocks = st.sidebar.multiselect(
    "Select Stocks",
    options=sorted(df["Stock"].unique()),
    default=sorted(df["Stock"].unique())
)

filtered_df = df[
    df["Stock"].isin(stocks)
]

# Summary

total_investment = filtered_df[
    "Investment"
].sum()

total_value = filtered_df[
    "Current_Value"
].sum()

total_profit = (
    total_value - total_investment
)

overall_return = (
    total_profit / total_investment
) * 100 if total_investment != 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Investment",
    f"₹{total_investment:,.2f}"
)

col2.metric(
    "Current Value",
    f"₹{total_value:,.2f}"
)

col3.metric(
    "Profit/Loss",
    f"₹{total_profit:,.2f}"
)

col4.metric(
    "Overall Return",
    f"{overall_return:.2f}%"
)

# Stock Performance

st.header("📊 Stock Performance")

stock_summary = filtered_df.groupby(
    ["Stock", "Sector"]
).agg(
    Investment=("Investment", "last"),
    Current_Value=("Current_Value", "last"),
    Profit_Loss=("Profit_Loss", "last"),
    Return_Percentage=("Return_Percentage", "last")
).reset_index()

st.dataframe(
    stock_summary,
    use_container_width=True
)

# Best and Worst

if not stock_summary.empty:

    best_stock = stock_summary.loc[
        stock_summary["Return_Percentage"].idxmax()
    ]

    worst_stock = stock_summary.loc[
        stock_summary["Return_Percentage"].idxmin()
    ]

    col1, col2 = st.columns(2)

    with col1:
        st.success(
            f"🏆 Best Stock: {best_stock['Stock']} "
            f"({best_stock['Return_Percentage']:.2f}%)"
        )

    with col2:
        st.error(
            f"📉 Worst Stock: {worst_stock['Stock']} "
            f"({worst_stock['Return_Percentage']:.2f}%)"
        )

# Portfolio Growth

st.header("📈 Portfolio Growth")

portfolio_growth = filtered_df.groupby(
    "Date"
).agg(
    Investment=("Investment", "sum"),
    Current_Value=("Current_Value", "sum")
)

fig, ax = plt.subplots()

ax.plot(
    portfolio_growth.index,
    portfolio_growth["Current_Value"],
    marker="o",
    label="Portfolio Value"
)

ax.plot(
    portfolio_growth.index,
    portfolio_growth["Investment"],
    linestyle="--",
    label="Investment"
)

ax.set_xlabel("Date")
ax.set_ylabel("Value (₹)")
ax.set_title("Portfolio Growth")
ax.legend()

plt.xticks(rotation=45)

st.pyplot(fig)

# Sector Investment

st.header("📊 Sector-wise Investment")

sector_data = filtered_df.groupby(
    "Sector"
)["Investment"].sum()

fig, ax = plt.subplots()

sector_data.plot(
    kind="bar",
    ax=ax
)

ax.set_title("Sector-wise Investment")
ax.set_xlabel("Sector")
ax.set_ylabel("Investment (₹)")

plt.xticks(rotation=45)

st.pyplot(fig)

# Daily Returns

st.header("📉 Daily Return Analysis")

daily_returns = filtered_df.groupby(
    "Date"
)["Daily_Return"].mean()

fig, ax = plt.subplots()

daily_returns.plot(
    kind="line",
    marker="o",
    ax=ax
)

ax.axhline(
    0,
    linestyle="--"
)

ax.set_title("Daily Returns")
ax.set_xlabel("Date")
ax.set_ylabel("Return (%)")

plt.xticks(rotation=45)

st.pyplot(fig)

# Moving Average

st.header("🔮 Moving Average Trend Prediction")

average_price = filtered_df.groupby(
    "Date"
)["Current_Price"].mean()

moving_average = average_price.rolling(
    window=3
).mean()

fig, ax = plt.subplots()

ax.plot(
    average_price.index,
    average_price,
    marker="o",
    label="Average Price"
)

ax.plot(
    moving_average.index,
    moving_average,
    linestyle="--",
    label="3-Day Moving Average"
)

ax.set_title("Moving Average Prediction")
ax.set_xlabel("Date")
ax.set_ylabel("Price (₹)")
ax.legend()

plt.xticks(rotation=45)

st.pyplot(fig)

if len(moving_average.dropna()) > 0:

    last_price = average_price.iloc[-1]
    last_ma = moving_average.dropna().iloc[-1]

    if last_price > last_ma:
        trend = "📈 UPWARD"
    elif last_price < last_ma:
        trend = "📉 DOWNWARD"
    else:
        trend = "➡️ SIDEWAYS"

    st.info(
        f"Predicted Next-Day Trend: **{trend}**"
    )