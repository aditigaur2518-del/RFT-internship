import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("D:\\Aditi\\RFT internship\\Day20\\sales_data.csv")

print("First 5 Rows:")
print(df.head())

print("\nDataset Info:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

df.drop_duplicates(inplace=True)

numeric_cols = df.select_dtypes(include=np.number).columns

for col in numeric_cols:
    df[col].fillna(df[col].mean(), inplace=True)

categorical_cols = df.select_dtypes(include='object').columns

for col in categorical_cols:
    df[col].fillna(df[col].mode()[0], inplace=True)

print("\nCleaned Dataset:")
print(df.head())

print("\nStatistical Summary:")
print(df.describe())

total_sales = df["Sales"].sum()
average_sales = df["Sales"].mean()
highest_sales = df["Sales"].max()
lowest_sales = df["Sales"].min()

print("\nSales Insights")
print("Total Sales:", total_sales)
print("Average Sales:", average_sales)
print("Highest Sales:", highest_sales)
print("Lowest Sales:", lowest_sales)

top_products = df.groupby("Product")["Sales"].sum().sort_values(ascending=False)

print("\nTop Products:")
print(top_products)

plt.figure(figsize=(10,5))
sns.barplot(x=top_products.index, y=top_products.values)
plt.title("Top Product Sales")
plt.xlabel("Products")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.show()

monthly_sales = df.groupby("Month")["Sales"].sum()

plt.figure(figsize=(10,5))
plt.plot(monthly_sales.index, monthly_sales.values, marker='o')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.grid(True)
plt.show()

plt.figure(figsize=(8,5))
sns.histplot(df["Sales"], bins=20, kde=True)
plt.title("Sales Distribution")
plt.xlabel("Sales")
plt.show()

plt.figure(figsize=(10,6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()

region_sales = df.groupby("Region")["Sales"].sum()

plt.figure(figsize=(8,5))
plt.pie(region_sales.values, labels=region_sales.index, autopct='%1.1f%%')
plt.title("Region Wise Sales Share")
plt.show()

print("\nWRITTEN SUMMARY")
print("1. Dataset cleaned successfully.")
print("2. Missing values handled using mean and mode.")
print("3. Duplicate values removed.")
print("4. Highest sales generating products identified.")
print("5. Monthly sales trend visualized.")
print("6. Region-wise contribution analyzed.")
print("7. Correlation between numerical features displayed.")

print("\nADVANCED INSIGHTS")
best_month = monthly_sales.idxmax()
worst_month = monthly_sales.idxmin()

print("Best Sales Month:", best_month)
print("Worst Sales Month:", worst_month)

best_region = region_sales.idxmax()
print("Top Performing Region:", best_region)

print("\nDashboard Style Output")
dashboard = pd.DataFrame({
    "Metric": [
        "Total Sales",
        "Average Sales",
        "Highest Sale",
        "Lowest Sale",
        "Top Region"
    ],
    "Value": [
        total_sales,
        average_sales,
        highest_sales,
        lowest_sales,
        best_region
    ]
})

print(dashboard)