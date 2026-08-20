import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Employee Performance Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Employee Performance Analytics System")
st.write("Analyze employee performance, attendance and department-wise statistics.")


st.sidebar.header("⚙️ Dashboard Settings")

uploaded_file = st.sidebar.file_uploader(
    "Upload Employee CSV Dataset",
    type=["csv"]
)
sample_data = pd.DataFrame({
    "Employee_ID": ["E001", "E002", "E003", "E004", "E005",
                    "E006", "E007", "E008", "E009", "E010",
                    "E011", "E012", "E013", "E014", "E015"],

    "Employee_Name": ["Aman", "Riya", "Rahul", "Priya", "Karan",
                      "Neha", "Rohit", "Anjali", "Vikas", "Simran",
                      "Arjun", "Pooja", "Mohit", "Kavya", "Nitin"],

    "Department": ["IT", "HR", "IT", "Finance", "Marketing",
                   "HR", "IT", "Finance", "Marketing", "IT",
                   "HR", "Finance", "Marketing", "IT", "HR"],

    "Performance": [88, 76, 95, 82, 91,
                    68, 97, 85, 79, 93,
                    72, 89, 81, 96, 74],

    "Attendance": [92, 85, 78, 96, 88,
                   72, 95, 69, 81, 90,
                   74, 94, 67, 98, 73]
})


if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ CSV file uploaded successfully!")

    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        st.stop()

else:
    st.info("ℹ️ No CSV uploaded. Sample employee data is being used.")
    df = sample_data.copy()

df.columns = (
    df.columns
    .str.strip()
    .str.replace(" ", "_")
    .str.lower()
)

def find_column(possible_names):

    for column in df.columns:

        column_clean = (
            column.lower()
            .replace("_", "")
            .replace(" ", "")
        )

        for name in possible_names:

            name_clean = (
                name.lower()
                .replace("_", "")
                .replace(" ", "")
            )

            if column_clean == name_clean:
                return column

    return None


employee_col = find_column([
    "employee_name",
    "name",
    "employee",
    "employeeid",
    "employee_id"
])

department_col = find_column([
    "department",
    "dept"
])

performance_col = find_column([
    "performance",
    "performance_score",
    "score",
    "rating",
    "performance_rating"
])

attendance_col = find_column([
    "attendance",
    "attendance_percentage",
    "attendance_percent"
])


missing_columns = []

if employee_col is None:
    missing_columns.append("Employee Name")

if department_col is None:
    missing_columns.append("Department")

if performance_col is None:
    missing_columns.append("Performance")

if attendance_col is None:
    missing_columns.append("Attendance")

if missing_columns:

    st.error("❌ Required columns are missing!")

    st.write("Missing columns:")
    for column in missing_columns:
        st.write(f"- {column}")

    st.write("Your CSV should contain columns similar to:")

    st.code("""
Employee_Name
Department
Performance
Attendance
    """)

    st.stop()


df[performance_col] = pd.to_numeric(
    df[performance_col],
    errors="coerce"
)

df[attendance_col] = pd.to_numeric(
    df[attendance_col],
    errors="coerce"
)

# Remove invalid rows
df = df.dropna(
    subset=[
        department_col,
        performance_col,
        attendance_col
    ]
)


st.sidebar.subheader("🔎 Filters")

departments = sorted(
    df[department_col].dropna().unique().tolist()
)

selected_departments = st.sidebar.multiselect(
    "Select Department",
    departments,
    default=departments
)

min_performance = st.sidebar.slider(
    "Minimum Performance",
    min_value=0,
    max_value=100,
    value=0
)

max_attendance = st.sidebar.slider(
    "Maximum Attendance",
    min_value=0,
    max_value=100,
    value=100
)


filtered_df = df[
    (df[department_col].isin(selected_departments))
    &
    (df[performance_col] >= min_performance)
    &
    (df[attendance_col] <= max_attendance)
].copy()


st.header("📌 Dashboard Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Employees",
        len(filtered_df)
    )

with col2:
    if len(filtered_df) > 0:
        avg_performance = filtered_df[performance_col].mean()
        st.metric(
            "Average Performance",
            f"{avg_performance:.2f}%"
        )
    else:
        st.metric("Average Performance", "0%")

with col3:
    if len(filtered_df) > 0:
        avg_attendance = filtered_df[attendance_col].mean()
        st.metric(
            "Average Attendance",
            f"{avg_attendance:.2f}%"
        )
    else:
        st.metric("Average Attendance", "0%")

with col4:
    low_attendance_count = len(
        filtered_df[
            filtered_df[attendance_col] < 75
        ]
    )

    st.metric(
        "Attendance Below 75%",
        low_attendance_count
    )


st.header("🏢 Department-wise Average Performance")

if len(filtered_df) > 0:

    department_average = (
        filtered_df
        .groupby(department_col)[performance_col]
        .mean()
        .reset_index()
    )

    department_average.columns = [
        "Department",
        "Average_Performance"
    ]

    department_average[
        "Average_Performance"
    ] = department_average[
        "Average_Performance"
    ].round(2)

    st.dataframe(
        department_average,
        use_container_width=True
    )

else:
    st.warning("No data available for the selected filters.")


st.header("🏆 Top 10 Performers")

top_10 = (
    filtered_df
    .sort_values(
        by=performance_col,
        ascending=False
    )
    .head(10)
)

top_columns = [
    employee_col,
    department_col,
    performance_col,
    attendance_col
]

st.dataframe(
    top_10[top_columns],
    use_container_width=True
)


st.header("⚠️ Employees with Attendance Below 75%")

low_attendance = (
    filtered_df[
        filtered_df[attendance_col] < 75
    ]
    .sort_values(
        by=attendance_col,
        ascending=True
    )
)

if len(low_attendance) > 0:

    st.dataframe(
        low_attendance[top_columns],
        use_container_width=True
    )

else:
    st.success(
        "🎉 No employees have attendance below 75%."
    )


st.header("📊 Performance Comparison Chart")

if len(department_average) > 0:

    fig1, ax1 = plt.subplots()

    ax1.bar(
        department_average["Department"],
        department_average["Average_Performance"]
    )

    ax1.set_title(
        "Department-wise Average Performance"
    )

    ax1.set_xlabel("Department")
    ax1.set_ylabel("Average Performance (%)")

    ax1.set_ylim(0, 100)

    plt.xticks(rotation=30)

    st.pyplot(fig1)

    plt.close(fig1)


st.header("📈 Attendance Trend")

if len(filtered_df) > 0:

    attendance_chart = (
        filtered_df
        .sort_values(by=attendance_col)
        .reset_index(drop=True)
    )

    fig2, ax2 = plt.subplots()

    ax2.plot(
        range(1, len(attendance_chart) + 1),
        attendance_chart[attendance_col],
        marker="o"
    )

    ax2.axhline(
        y=75,
        linestyle="--",
        label="75% Attendance Limit"
    )

    ax2.set_title(
        "Employee Attendance Trend"
    )

    ax2.set_xlabel("Employee")
    ax2.set_ylabel("Attendance (%)")

    ax2.set_ylim(0, 100)

    ax2.legend()

    st.pyplot(fig2)

    plt.close(fig2)


st.header("🥧 Department Distribution")

department_distribution = (
    filtered_df[department_col]
    .value_counts()
)

if len(department_distribution) > 0:

    fig3, ax3 = plt.subplots()

    ax3.pie(
        department_distribution.values,
        labels=department_distribution.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax3.set_title(
        "Employee Distribution by Department"
    )

    st.pyplot(fig3)

    plt.close(fig3)


st.header("⭐ Performance Classification")

def performance_category(score):

    if score >= 90:
        return "Excellent"

    elif score >= 75:
        return "Good"

    elif score >= 60:
        return "Average"

    else:
        return "Needs Improvement"


filtered_df["Performance_Category"] = (
    filtered_df[performance_col]
    .apply(performance_category)
)

category_distribution = (
    filtered_df["Performance_Category"]
    .value_counts()
    .reset_index()
)

category_distribution.columns = [
    "Performance_Category",
    "Employee_Count"
]

st.dataframe(
    category_distribution,
    use_container_width=True
)


st.header("📄 Final Employee Performance Report")

final_report = filtered_df.copy()

final_report["Performance_Category"] = (
    final_report[performance_col]
    .apply(performance_category)
)


final_report = final_report.rename(
    columns={
        employee_col: "Employee_Name",
        department_col: "Department",
        performance_col: "Performance",
        attendance_col: "Attendance"
    }
)

 
report_columns = [
    "Employee_Name",
    "Department",
    "Performance",
    "Attendance",
    "Performance_Category"
]


report_columns = [
    col for col in report_columns
    if col in final_report.columns
]

final_report = final_report[report_columns]

st.dataframe(
    final_report,
    use_container_width=True
)


csv_data = final_report.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Final Report as CSV",
    data=csv_data,
    file_name="employee_performance_final_report.csv",
    mime="text/csv"
)


top10_csv = top_10[
    top_columns
].to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="🏆 Download Top 10 Performers",
    data=top10_csv,
    file_name="top_10_performers.csv",
    mime="text/csv"
)


low_attendance_csv = low_attendance[
    top_columns
].to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⚠️ Download Low Attendance Report",
    data=low_attendance_csv,
    file_name="low_attendance_report.csv",
    mime="text/csv"
)


with st.expander("📋 View Complete Dataset"):

    st.dataframe(
        df,
        use_container_width=True
    )


st.markdown("---")

st.markdown(
    """
    ### 📊 Employee Performance Analytics System

    **Features:** CSV Import • Performance Analysis •
    Attendance Analysis • Top Performers • Charts •
    Department Distribution • CSV Export • Interactive Filters

    **Built using:** Python • Pandas • Matplotlib • Streamlit
    """
)