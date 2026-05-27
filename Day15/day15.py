import pandas as pd
import matplotlib.pyplot as plt

data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"],
    "Sales": [1200, 1500, 1800, 1700, 2100, 2500, 2400, 3000],
    "Profit": [200, 300, 350, 320, 500, 650, 600, 800],
    "Customers": [50, 65, 80, 75, 95, 120, 115, 140]
}

df = pd.DataFrame(data)

print("DATASET\n")
print(df)

print("\nDATASET SUMMARY\n")
print(df.describe())

highest_sales = df[df["Sales"] == df["Sales"].max()]
lowest_sales = df[df["Sales"] == df["Sales"].min()]

print("\nHIGHEST SALES MONTH\n")
print(highest_sales[["Month", "Sales"]])

print("\nLOWEST SALES MONTH\n")
print(lowest_sales[["Month", "Sales"]])

avg_sales = df["Sales"].mean()
outliers = df[df["Sales"] > avg_sales * 1.3]

print("\nPOSSIBLE OUTLIERS IN SALES\n")
print(outliers)

plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.plot(df["Month"], df["Sales"], marker='o')
plt.title("Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")

plt.subplot(1, 3, 2)
plt.bar(df["Month"], df["Profit"])
plt.title("Profit Comparison")
plt.xlabel("Month")
plt.ylabel("Profit")

plt.subplot(1, 3, 3)
plt.hist(df["Customers"], bins=5)
plt.title("Customer Distribution")
plt.xlabel("Customers")
plt.ylabel("Frequency")

plt.tight_layout()
plt.show()

print("\nINSIGHTS\n")

print("1. Sales show a continuous upward trend over the months.")
print("2. Profit increases along with sales, showing business growth.")
print("3. Customer count is mostly concentrated between medium to high values.")
print("4. August recorded the highest sales and profit.")
print("5. Higher customer count appears to contribute to increased sales.")
print("6. Months with extremely high sales are detected as visual outliers.")