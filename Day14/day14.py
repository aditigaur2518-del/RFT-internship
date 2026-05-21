
import matplotlib.pyplot as plt


categories = ["FOOD", "TRAVEL", "SHOPPING"]
expenses = [500, 300, 200]


colors = ["gold", "skyblue", "lightgreen"]


explode = [0.1, 0, 0]   


plt.pie(
    expenses,
    labels=categories,
    colors=colors,
    explode=explode,
    autopct='%1.1f%%',   
    startangle=90
)


plt.title("Category Breakdown of Expenses")


plt.show()