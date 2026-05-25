

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


data = {
    "Date": [
        "2025-01-01", "2025-01-05", "2025-01-10",
        "2025-02-01", "2025-02-08", "2025-02-15",
        "2025-03-01", "2025-03-10", "2025-03-18",
        "2025-04-01"
    ],
    
    "Product": [
        "Laptop", "Mobile", "Tablet",
        "Laptop", "Mobile", "Tablet",
        "Laptop", "Mobile", "Tablet",
        "Laptop"
    ],
    
    "Region": [
        "North", "South", "East",
        "West", "North", "South",
        "East", "West", "North",
        "South"
    ],
    
    "Sales": [
        50000, 30000, np.nan,
        45000, 25000, 20000,
        55000, np.nan, 35000,
        60000
    ]
}


df = pd.DataFrame(data)

df["Date"] = pd.to_datetime(df["Date"])


print("\n===== ORIGINAL DATASET =====")
print(df)

df["Sales"] = df["Sales"].fillna(df["Sales"].mean())

print("\n===== DATA AFTER HANDLING MISSING VALUES =====")
print(df)



product_sales = df.groupby("Product")["Sales"].sum()

print("\n===== TOTAL SALES PER PRODUCT =====")
print(product_sales)



region_sales = df.groupby("Region")["Sales"].sum()

print("\n===== REGION-WISE SALES PERFORMANCE =====")
print(region_sales)


monthly_sales = df.groupby("Date")["Sales"].sum()

plt.figure(figsize=(10, 5))
plt.plot(monthly_sales.index, monthly_sales.values, marker='o')

plt.title("Sales Trend Over Time")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.grid(True)

plt.show()



plt.figure(figsize=(8, 5))
product_sales.sort_values(ascending=False).plot(kind='bar')

plt.title("Top Products by Sales")
plt.xlabel("Product")
plt.ylabel("Total Sales")

plt.show()

df["Month"] = df["Date"].dt.month_name()

monthly_growth = df.groupby("Month")["Sales"].sum()

print("\n===== MONTHLY GROWTH ANALYSIS =====")
print(monthly_growth)



best_region = region_sales.idxmax()

print("\n===== BEST PERFORMING REGION =====")
print("Best Region:", best_region)



print("\n===== KEY INSIGHTS =====")


top_product = product_sales.idxmax()
print(f"1. Highest selling product is {top_product}.")


print(f"2. Best performing region is {best_region}.")


highest_sales = df["Sales"].max()
print(f"3. Highest single sale recorded is {highest_sales}.")


lowest_sales = df["Sales"].min()
print(f"4. Lowest sale recorded is {lowest_sales}.")


average_sales = df["Sales"].mean()
print(f"5. Average sales value is {average_sales:.2f}.")