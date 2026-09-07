import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("expense_data.csv")

df["Date"] = pd.to_datetime(df["Date"])

df["Month"] = df["Date"].dt.to_period("M").astype(str)


def categorize(description):
    description = description.lower()

    if "rent" in description:
        return "Housing"

    elif "grocery" in description or "restaurant" in description:
        return "Food"

    elif "electricity" in description or "internet" in description:
        return "Utilities"

    elif "transport" in description:
        return "Transport"

    elif "shopping" in description:
        return "Shopping"

    elif "medicine" in description:
        return "Healthcare"

    else:
        return "Other"


df["Category"] = df["Description"].apply(categorize)


income = df[df["Type"] == "Income"]["Amount"].sum()

expenses = df[df["Type"] == "Expense"]["Amount"].sum()

savings = income - expenses

savings_percentage = (savings / income) * 100


print("\n" + "=" * 50)
print("       SMART EXPENSE TRACKER")
print("=" * 50)

print(f"\nTotal Income   : ₹{income:,.2f}")
print(f"Total Expenses : ₹{expenses:,.2f}")
print(f"Total Savings  : ₹{savings:,.2f}")
print(f"Savings Rate   : {savings_percentage:.2f}%")


print("\nCATEGORY-WISE EXPENSES")
print("-" * 50)

category_expenses = (
    df[df["Type"] == "Expense"]
    .groupby("Category")["Amount"]
    .sum()
    .sort_values(ascending=False)
)

print(category_expenses)


budget = 30000

print("\nBUDGET ANALYSIS")
print("-" * 50)

if expenses <= budget:
    print(f"Budget : ₹{budget:,.2f}")
    print("Status : Within Budget")
else:
    print(f"Budget : ₹{budget:,.2f}")
    print("Status : Over Budget")


monthly_expenses = (
    df[df["Type"] == "Expense"]
    .groupby("Month")["Amount"]
    .sum()
)

print("\nMONTHLY EXPENSES")
print("-" * 50)

print(monthly_expenses)


predicted_expense = monthly_expenses.tail(3).mean()

print("\nEXPENSE PREDICTION")
print("-" * 50)

print(
    f"Predicted Next Month Expense : "
    f"₹{predicted_expense:,.2f}"
)


plt.figure(figsize=(10, 5))

plt.plot(
    monthly_expenses.index,
    monthly_expenses.values,
    marker="o"
)

plt.title("Monthly Spending Trend")
plt.xlabel("Month")
plt.ylabel("Expenses (₹)")
plt.grid(True)

plt.savefig("spending_trend.png")

plt.show()


plt.figure(figsize=(10, 5))

category_expenses.plot(kind="bar")

plt.title("Expenses by Category")
plt.xlabel("Category")
plt.ylabel("Amount (₹)")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("category_expenses.png")

plt.show()


df.to_csv(
    "final_expense_report.csv",
    index=False
)

print("\nFinal report saved as:")
print("final_expense_report.csv")

print("\nProject completed successfully!")