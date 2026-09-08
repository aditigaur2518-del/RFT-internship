
import pandas as pd
from datetime import datetime

input_file = "invoices.csv"
output_file = "consolidated_invoice_report.csv"

df = pd.read_csv(input_file)

df["Total_Amount"] = df["Quantity"] * df["Price"]

today = datetime.today()

df["Due_Date"] = pd.to_datetime(df["Due_Date"])

df["Status"] = df["Due_Date"].apply(
    lambda date: "Overdue" if date < today else "Pending"
)

report = df[
    [
        "Invoice_Number",
        "Customer_Name",
        "Customer_Email",
        "Invoice_Date",
        "Due_Date",
        "Item",
        "Quantity",
        "Price",
        "Total_Amount",
        "Status"
    ]
]

report.to_csv(output_file, index=False)

print("\n========== AUTOMATED INVOICE PROCESSING SYSTEM ==========\n")

print("Total Invoices:", len(report))
print("Total Invoice Amount: ₹", report["Total_Amount"].sum())
print("Overdue Invoices:", (report["Status"] == "Overdue").sum())
print("Pending Invoices:", (report["Status"] == "Pending").sum())

print("\n========== INVOICE REPORT ==========\n")

print(report.to_string(index=False))

print("\nReport generated successfully!")
print("File:", output_file)



