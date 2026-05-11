import pandas as pd
import io

csv_data = """PRODUCT,QUANTITY,PRICE
A,2,100
B,1,200
A,3,100
C,5,50"""


df = pd.read_csv(io.StringIO(csv_data))


df['TOTAL'] = df['QUANTITY'] * df['PRICE']

product_summary = df.groupby('PRODUCT').agg({
    'QUANTITY': 'sum', 
    'TOTAL': 'sum'
}).reset_index()


product_summary = product_summary.sort_values(by='TOTAL', ascending=False)


total_revenue = df['TOTAL'].sum()


top_selling_idx = product_summary['QUANTITY'].idxmax()
top_selling_product = product_summary.loc[top_selling_idx, 'PRODUCT']


print("--- Sales Data with Total Column ---")
print(df)

print("\n--- Summary (Sorted by Revenue) ---")
print(product_summary)

print(f"\nTotal Revenue: {total_revenue}")
print(f"Top-Selling Product: {top_selling_product}")