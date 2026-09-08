
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Invoice Processing System",
    page_icon="🧾"
)

st.title("🧾 Automated Invoice Processing System")
st.write("Welcome to the Invoice Dashboard!")

try:
    df = pd.read_csv("invoices.csv")

    df["Total_Amount"] = df["Quantity"] * df["Price"]

    st.subheader("📊 Invoice Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Invoices", len(df))

    with col2:
        st.metric("Total Amount", f"₹{df['Total_Amount'].sum():,.2f}")

    with col3:
        st.metric("Average Invoice", f"₹{df['Total_Amount'].mean():,.2f}")

    st.subheader("📋 Invoice Details")

    st.dataframe(df, use_container_width=True)

    st.success("Invoice data loaded successfully!")

except FileNotFoundError:
    st.error("invoices.csv was not found. Make sure it is in the same folder as app.py.")


 