import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰"
)

st.title("💰 Smart Expense Tracker & Budget Analyzer")

st.write(
    "Analyze your income, expenses, savings and budget."
)


uploaded_file = st.file_uploader(
    "Upload Expense CSV File",
    type=["csv"]
)


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


if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    df["Date"] = pd.to_datetime(df["Date"])

    df["Month"] = (
        df["Date"]
        .dt.to_period("M")
        .astype(str)
    )

    df["Category"] = (
        df["Description"]
        .apply(categorize)
    )


    income = df[
        df["Type"] == "Income"
    ]["Amount"].sum()


    expenses = df[
        df["Type"] == "Expense"
    ]["Amount"].sum()


    savings = income - expenses


    if income > 0:

        savings_percentage = (
            savings / income
        ) * 100

    else:

        savings_percentage = 0


    st.subheader("📊 Financial Summary")


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Total Income",
        f"₹{income:,.2f}"
    )


    col2.metric(
        "Total Expenses",
        f"₹{expenses:,.2f}"
    )


    col3.metric(
        "Total Savings",
        f"₹{savings:,.2f}"
    )


    st.write(
        f"**Savings Rate:** "
        f"{savings_percentage:.2f}%"
    )


    st.divider()


    st.subheader("💰 Budget Analysis")


    budget = st.number_input(
        "Enter Monthly Budget",
        min_value=0,
        value=30000
    )


    if expenses <= budget:

        st.success(
            f"Within Budget ✅ "
            f"(₹{budget - expenses:,.2f} remaining)"
        )

    else:

        st.error(
            f"Over Budget ❌ "
            f"(₹{expenses - budget:,.2f} exceeded)"
        )


    st.divider()


    st.subheader("📈 Monthly Spending Trend")


    monthly_expenses = (
        df[df["Type"] == "Expense"]
        .groupby("Month")["Amount"]
        .sum()
    )


    fig, ax = plt.subplots()


    ax.plot(
        monthly_expenses.index,
        monthly_expenses.values,
        marker="o"
    )


    ax.set_title(
        "Monthly Spending Trend"
    )

    ax.set_xlabel("Month")

    ax.set_ylabel(
        "Expenses (₹)"
    )

    ax.grid(True)


    st.pyplot(fig)


    st.divider()


    st.subheader("🏷️ Expenses by Category")


    category_expenses = (
        df[df["Type"] == "Expense"]
        .groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )


    fig2, ax2 = plt.subplots()


    category_expenses.plot(
        kind="bar",
        ax=ax2
    )


    ax2.set_title(
        "Expenses by Category"
    )

    ax2.set_xlabel("Category")

    ax2.set_ylabel(
        "Amount (₹)"
    )


    plt.xticks(rotation=45)


    st.pyplot(fig2)


    st.divider()


    st.subheader("🥧 Spending Distribution")


    fig3, ax3 = plt.subplots()


    category_expenses.plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax3
    )


    ax3.set_ylabel("")


    st.pyplot(fig3)


    st.divider()


    st.subheader("🔮 Expense Prediction")


    if len(monthly_expenses) >= 2:

        prediction = (
            monthly_expenses
            .tail(3)
            .mean()
        )

        st.info(
            f"Predicted Next Month Expense: "
            f"₹{prediction:,.2f}"
        )

    else:

        st.warning(
            "Not enough data for prediction."
        )


    st.divider()


    st.subheader("📋 Expense Data")

    st.dataframe(
        df,
        use_container_width=True
    )


    st.download_button(
        "📥 Download Final Report",
        df.to_csv(index=False),
        "final_expense_report.csv",
        "text/csv"
    )


else:

    st.info(
        "👆 Upload expense_data.csv to start."
    )