import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

df = pd.read_csv("social_media_data.csv")

df["Engagement"] = df["Likes"] + df["Comments"] + df["Shares"]

hashtags = []

for tags in df["Hashtags"]:
    hashtags.extend(tags.split())

hashtag_count = Counter(hashtags)

top_hashtags = pd.DataFrame(
    hashtag_count.most_common(10),
    columns=["Hashtag", "Count"]
)

active_users = df["Username"].value_counts()

popular_time = df.groupby("Time")["Engagement"].sum().idxmax()

daily_engagement = df.groupby("Date")["Engagement"].sum()

category_count = df["Category"].value_counts()

report = pd.DataFrame({
    "Metric": [
        "Total Posts",
        "Total Likes",
        "Total Comments",
        "Total Shares",
        "Total Engagement",
        "Most Popular Posting Time",
        "Most Active User"
    ],
    "Value": [
        len(df),
        df["Likes"].sum(),
        df["Comments"].sum(),
        df["Shares"].sum(),
        df["Engagement"].sum(),
        popular_time,
        active_users.idxmax()
    ]
})

report.to_csv("analytics_report.csv", index=False)

print("\n===== SOCIAL MEDIA TREND ANALYZER =====")

print("\nTop Trending Hashtags:")
print(top_hashtags)

print("\nMost Active Users:")
print(active_users)

print("\nTotal Engagement:", df["Engagement"].sum())

print("\nMost Popular Posting Time:", popular_time)

print("\nAnalytics report saved as analytics_report.csv")


plt.figure(figsize=(8, 5))
plt.bar(top_hashtags["Hashtag"], top_hashtags["Count"])
plt.title("Top Trending Hashtags")
plt.xlabel("Hashtag")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("top_hashtags.png")
plt.show()


plt.figure(figsize=(8, 5))
plt.plot(daily_engagement.index, daily_engagement.values, marker="o")
plt.title("Daily Engagement Trend")
plt.xlabel("Date")
plt.ylabel("Engagement")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("daily_engagement.png")
plt.show()


plt.figure(figsize=(7, 7))
plt.pie(
    category_count.values,
    labels=category_count.index,
    autopct="%1.1f%%"
)
plt.title("Content Category Distribution")
plt.savefig("category_distribution.png")
plt.show()