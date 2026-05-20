

import matplotlib.pyplot as plt
import numpy as np

students = ["AMIT", "RIYA", "JOHN"]

maths_marks = [85, 92, 78]
science_marks = [80, 88, 75]
english_marks = [78, 90, 82]


x = np.arange(len(students))
width = 0.25


plt.figure(figsize=(10, 6))


plt.bar(x - width, maths_marks, width, label="Maths")
plt.bar(x, science_marks, width, label="Science")
plt.bar(x + width, english_marks, width, label="English")

plt.title("Student Performance Dashboard")
plt.xlabel("Students")
plt.ylabel("Marks")


plt.xticks(x, students)


plt.legend()


for i in range(len(students)):
    plt.text(x[i] - width, maths_marks[i] + 1, str(maths_marks[i]), ha='center')
    plt.text(x[i], science_marks[i] + 1, str(science_marks[i]), ha='center')
    plt.text(x[i] + width, english_marks[i] + 1, str(english_marks[i]), ha='center')


plt.grid(axis='y', linestyle='--', alpha=0.5)


plt.show()