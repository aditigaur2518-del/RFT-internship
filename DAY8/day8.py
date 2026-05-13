import pandas as pd


data = {
    "NAME": ["A", "B", "C", "D"],
    "DEPT": ["IT", "HR", "IT", "HR"],
    "SALARY": [50000, 40000, 60000, 45000]
}

df = pd.DataFrame(data)

print("Employee Dataset:\n")
print(df)


avg_salary = df.groupby("DEPT")["SALARY"].mean()

print("\nAverage Salary Per Department:\n")
print(avg_salary)


highest_paid = df.loc[df.groupby("DEPT")["SALARY"].idxmax()]

print("\nHighest Paid Employee Per Department:\n")
print(highest_paid)

employee_count = df.groupby("DEPT")["NAME"].count()

print("\nEmployee Count Per Department:\n")
print(employee_count)


sorted_departments = avg_salary.sort_values(ascending=False)

print("\nDepartments Sorted By Average Salary:\n")
print(sorted_departments)
