import pandas as pd

data = {
    "NAME": ["AMIT", "RIYA", "JOHN"],
    "MATH": [80, 90, 60],
    "SCIENCE": [70, 88, 65],
    "ENGLISH": [85, 92, 70]
}

df = pd.DataFrame(data)

df["AVERAGE"] = (df["MATH"] + df["SCIENCE"] + df["ENGLISH"]) / 3

def grade(avg):
    if avg >= 90:
        return "A+"
    elif avg >= 75:
        return "A"
    elif avg >= 60:
        return "B"
    else:
        return "C"

df["GRADE"] = df["AVERAGE"].apply(grade)

topper = df.loc[df["AVERAGE"].idxmax()]

overall_avg = df["AVERAGE"].mean()

above_avg = df[df["AVERAGE"] > overall_avg]

subject_avg = df[["MATH", "SCIENCE", "ENGLISH"]].mean()

print("STUDENT PERFORMANCE DASHBOARD\n")

print(df)

print("\nTOPPER:")
print(topper["NAME"], "-", topper["AVERAGE"])

print("\nNUMBER OF STUDENTS ABOVE AVERAGE:")
print(len(above_avg))

print("\nSUBJECT-WISE AVERAGE:")
print(subject_avg)