
import matplotlib.pyplot as plt
import numpy as np

students = ["AMIT", "RIYA", "JOHN"]

maths = [85, 92, 78]
science = [88, 95, 80]
english = [82, 89, 76]

x = np.arange(len(students))
width = 0.25

plt.figure(figsize=(10, 6))

plt.bar(x - width, maths, width=width, label="Maths")
plt.bar(x, science, width=width, label="Science")
plt.bar(x + width, english, width=width, label="English")

plt.xlabel("Students")
plt.ylabel("Marks")
plt.title("Student Performance Dashboard")

plt.xticks(x, students)

plt.legend()

for i in range(len(students)):
    plt.text(x[i] - width, maths[i] + 1, str(maths[i]), ha='center')
    plt.text(x[i], science[i] + 1, str(science[i]), ha='center')
    plt.text(x[i] + width, english[i] + 1, str(english[i]), ha='center')


plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()