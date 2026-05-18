import matplotlib.pyplot as plt

days = ['MON', 'TUE', 'WED', 'THU', 'FRI']
sales = [200, 260, 300, 280, 360]


highest_sale = max(sales)
lowest_sale = min(sales)

highest_day = days[sales.index(highest_sale)]
lowest_day = days[sales.index(lowest_sale)]


plt.figure(figsize=(8, 5))

plt.plot(days, sales, marker='o', linestyle='-', color='blue', label='Sales Trend')


plt.scatter(highest_day, highest_sale, color='green', s=100, label='Highest Sale')


plt.scatter(lowest_day, lowest_sale, color='red', s=100, label='Lowest Sale')


plt.xlabel("Days")
plt.ylabel("Sales")
plt.title("Weekly Sales Trend Visualization")


plt.grid(True)
plt.legend()


for i in range(len(days)):
    plt.text(days[i], sales[i] + 5, str(sales[i]), ha='center')


plt.show()


print("Trend Analysis:")
print(f"Highest Sales: {highest_sale} on {highest_day}")
print(f"Lowest Sales: {lowest_sale} on {lowest_day}")

if sales[-1] > sales[0]:
    print("Overall sales trend is increasing.")
else:
    print("Overall sales trend is decreasing.")