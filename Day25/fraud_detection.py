import pandas as pd
import matplotlib.pyplot as plt
import os

# ==============================
# CONFIGURATION
# ==============================

FILE_NAME = "transactions.csv"
HIGH_VALUE_THRESHOLD = 50000
FREQUENT_TRANSACTION_THRESHOLD = 5

# ==============================
# READ CSV FILE
# ==============================

if not os.path.exists(FILE_NAME):
    print(f"Error: {FILE_NAME} not found.")
    exit()

df = pd.read_csv(FILE_NAME)

# ==============================
# DATA CLEANING
# ==============================

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

df.dropna(subset=["Transaction_ID", "Account_ID", "Date", "Amount"], inplace=True)

df.drop_duplicates(inplace=True)

# ==============================
# DETECT DUPLICATE TRANSACTIONS
# ==============================

duplicates = df[df.duplicated(
    subset=["Account_ID", "Date", "Amount", "Category"],
    keep=False
)].copy()

duplicates.to_csv("duplicate_transactions.csv", index=False)

# ==============================
# IDENTIFY HIGH-VALUE TRANSACTIONS
# ==============================

high_value = df[df["Amount"] > HIGH_VALUE_THRESHOLD].copy()

high_value.to_csv("high_value_transactions.csv", index=False)

# ==============================
# FIND FREQUENTLY ACTIVE ACCOUNTS
# ==============================

account_transaction_count = df["Account_ID"].value_counts()

frequent_accounts = account_transaction_count[
    account_transaction_count >= FREQUENT_TRANSACTION_THRESHOLD
]

# ==============================
# CREATE RISK SCORE
# ==============================

def calculate_risk_score(row):
    score = 0

    if row["Amount"] > 100000:
        score += 50
    elif row["Amount"] > HIGH_VALUE_THRESHOLD:
        score += 30

    if row["Account_ID"] in frequent_accounts.index:
        score += 20

    if row["Payment_Method"] == "Card" and row["Amount"] > HIGH_VALUE_THRESHOLD:
        score += 15

    if score >= 70:
        risk_level = "High"
    elif score >= 40:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return pd.Series([score, risk_level])


df[["Risk_Score", "Risk_Level"]] = df.apply(
    calculate_risk_score,
    axis=1
)

# ==============================
# IDENTIFY SUSPICIOUS TRANSACTIONS
# ==============================

suspicious_transactions = df[
    (df["Risk_Score"] >= 40)
].copy()

suspicious_transactions.to_csv(
    "suspicious_transactions.csv",
    index=False
)

# ==============================
# DAILY TRANSACTION TREND
# ==============================

daily_transactions = df.groupby("Date")["Amount"].sum()

plt.figure(figsize=(12, 6))
plt.plot(
    daily_transactions.index,
    daily_transactions.values,
    marker="o"
)

plt.title("Daily Transaction Trend")
plt.xlabel("Date")
plt.ylabel("Total Transaction Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("daily_transaction_trend.png")
plt.show()

# ==============================
# TRANSACTION CATEGORY CHART
# ==============================

category_amount = df.groupby("Category")["Amount"].sum()

plt.figure(figsize=(10, 6))
plt.bar(
    category_amount.index,
    category_amount.values
)

plt.title("Transaction Category Chart")
plt.xlabel("Category")
plt.ylabel("Total Transaction Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("transaction_category_chart.png")
plt.show()

# ==============================
# TOP 10 HIGHEST TRANSACTIONS
# ==============================

top_10 = df.nlargest(10, "Amount")

plt.figure(figsize=(12, 6))
plt.bar(
    top_10["Transaction_ID"],
    top_10["Amount"]
)

plt.title("Top 10 Highest Transactions")
plt.xlabel("Transaction ID")
plt.ylabel("Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("top_10_transactions.png")
plt.show()

# ==============================
# EXPORT COMPLETE ANALYSIS
# ==============================

df.to_csv(
    "transaction_analysis_report.csv",
    index=False
)

# ==============================
# DISPLAY RESULTS
# ==============================

print("\n" + "=" * 60)
print("       FRAUD DETECTION & TRANSACTION ANALYSIS")
print("=" * 60)

print(f"\nTotal Transactions: {len(df)}")

print(f"Total Transaction Amount: ₹{df['Amount'].sum():,.2f}")

print(
    f"Average Transaction Amount: "
    f"₹{df['Amount'].mean():,.2f}"
)

print(
    f"\nDuplicate Transactions: "
    f"{len(duplicates)}"
)

print(
    f"High-Value Transactions: "
    f"{len(high_value)}"
)

print(
    f"Suspicious Transactions: "
    f"{len(suspicious_transactions)}"
)

print("\nFrequent Transaction Accounts:")
print(frequent_accounts)

print("\nTop 10 Highest Transactions:")
print(
    top_10[
        [
            "Transaction_ID",
            "Account_ID",
            "Amount",
            "Category",
            "Risk_Score",
            "Risk_Level"
        ]
    ].to_string(index=False)
)

print("\nSuspicious Transactions:")
print(
    suspicious_transactions[
        [
            "Transaction_ID",
            "Account_ID",
            "Amount",
            "Category",
            "Risk_Score",
            "Risk_Level"
        ]
    ].to_string(index=False)
)

print("\nFiles Generated:")
print("1. duplicate_transactions.csv")
print("2. high_value_transactions.csv")
print("3. suspicious_transactions.csv")
print("4. transaction_analysis_report.csv")
print("5. daily_transaction_trend.png")
print("6. transaction_category_chart.png")
print("7. top_10_transactions.png")

print("\nAnalysis completed successfully!")