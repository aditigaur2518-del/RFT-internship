import pandas as pd
import matplotlib.pyplot as plt

data = {
    "Customer_ID": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    "Age": [22, 35, 26, 45, 52, 23, 40, 31, 28, 50],
    "Spending": [2500, 12000, 5000, 18000, 22000, 3000, 15000, 7000, 4000, 25000],
    "Visits": [5, 20, 8, 25, 30, 4, 18, 10, 6, 35]
}

df = pd.DataFrame(data)

def spending_category(amount):
    if amount >= 15000:
        return "High"
    elif amount >= 7000:
        return "Medium"
    else:
        return "Low"

df["Category"] = df["Spending"].apply(spending_category)

high_value_customers = df[(df["Spending"] >= 15000) & (df["Visits"] >= 15)]

low_engagement_users = df[df["Visits"] < 7]

print("Customer Segmentation Data")
print(df)

print("\nHigh Value Customers")
print(high_value_customers)

print("\nLow Engagement Users")
print(low_engagement_users)

print("\nBusiness Strategies")

for category in df["Category"].unique():
    if category == "High":
        print("High: Offer premium memberships and exclusive rewards")
    elif category == "Medium":
        print("Medium: Provide discounts and personalized recommendations")
    else:
        print("Low: Send promotional offers to increase engagement")

plt.figure(figsize=(8, 5))
plt.hist(df["Spending"], bins=5)
plt.title("Spending Distribution")
plt.xlabel("Spending")
plt.ylabel("Number of Customers")
plt.show()

category_counts = df["Category"].value_counts()

plt.figure(figsize=(6, 6))
plt.pie(category_counts, labels=category_counts.index, autopct="%1.1f%%")
plt.title("Customer Categories")
plt.show()