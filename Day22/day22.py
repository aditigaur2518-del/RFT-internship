import pandas as pd
import matplotlib.pyplot as plt



file_name = "sales_data.csv"

df = pd.read_csv(file_name)

print("Original Dataset:")
print(df.head())
print("\nDataset Shape:", df.shape)





df = df.drop_duplicates()


print("\nMissing Values:")
print(df.isnull().sum())


df = df.dropna(subset=["Customer", "Product", "Category", "Sales"])


df["Date"] = pd.to_datetime(df["Date"], errors="coerce")


df = df.dropna(subset=["Date"])


df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")


df = df.dropna(subset=["Sales"])

print("\nCleaned Dataset:")
print(df.head())
print("\nCleaned Dataset Shape:", df.shape)



total_sales = df["Sales"].sum()

print("\n================================")
print("SALES SUMMARY")
print("================================")

print("Total Sales: ₹", round(total_sales, 2))




average_revenue = df["Sales"].mean()

print("Average Revenue per Transaction: ₹",
      round(average_revenue, 2))



top_customers = (
    df.groupby("Customer")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print("\n================================")
print("TOP 5 CUSTOMERS")
print("================================")

print(top_customers)




daily_sales = (
    df.groupby("Date")["Sales"]
    .sum()
    .sort_index()
)

plt.figure(figsize=(10, 5))

plt.plot(
    daily_sales.index,
    daily_sales.values,
    marker="o"
)

plt.title("Sales Trend Over Time")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()




top_products = (
    df.groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 5))

plt.bar(
    top_products.index,
    top_products.values
)

plt.title("Top Products by Sales")
plt.xlabel("Product")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()




category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
)

plt.figure(figsize=(7, 7))

plt.pie(
    category_sales.values,
    labels=category_sales.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Sales Distribution by Category")
plt.tight_layout()
plt.show()



best_product = top_products.index[0]
best_product_sales = top_products.iloc[0]


best_category = category_sales.idxmax()
best_category_sales = category_sales.max()


total_customers = df["Customer"].nunique()


total_products = df["Product"].nunique()

print("\n================================")
print("BUSINESS SUMMARY")
print("================================")

print("Total Sales: ₹", round(total_sales, 2))
print("Average Revenue: ₹", round(average_revenue, 2))
print("Total Customers:", total_customers)
print("Total Products:", total_products)

print(
    "Best-Selling Product:",
    best_product,
    "with sales of ₹",
    round(best_product_sales, 2)
)

print(
    "Best Performing Category:",
    best_category,
    "with sales of ₹",
    round(best_category_sales, 2)
)




print("\n================================")
print("5 BUSINESS INSIGHTS")
print("================================")

print(
    f"1. The total sales generated were ₹{total_sales:,.2f}, "
    f"showing the overall revenue performance."
)

print(
    f"2. The average revenue per transaction was "
    f"₹{average_revenue:,.2f}."
)

print(
    f"3. The top 5 customers contributed significantly "
    f"to the overall sales and can be targeted for loyalty programs."
)

print(
    f"4. {best_product} was the best-selling product, "
    f"generating ₹{best_product_sales:,.2f} in sales."
)

print(
    f"5. {best_category} was the highest-performing category, "
    f"with total sales of ₹{best_category_sales:,.2f}."
)