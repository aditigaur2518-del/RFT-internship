
marks = [78, 85, 90, 67, 85, 92, 78]


average = sum(marks) / len(marks)


highest = max(marks)
lowest = min(marks)


above_avg_count = 0
for mark in marks:
    if mark > average:
        above_avg_count += 1


grades = {"A": 0, "B": 0, "C": 0, "Fail": 0}

for mark in marks:
    if mark >= 90:
        grades["A"] += 1
    elif mark >= 75:
        grades["B"] += 1
    elif mark >= 50:
        grades["C"] += 1
    else:
        grades["Fail"] += 1


print("Average Marks:", average)
print("Highest Marks:", highest)
print("Lowest Marks:", lowest)
print("Students Above Average:", above_avg_count)
print("Grade Distribution:", grades)