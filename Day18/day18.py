import pandas as pd
import matplotlib.pyplot as plt

data = {
    "Movie_Name": [
        "Inception",
        "Avengers",
        "Titanic",
        "Joker",
        "Interstellar",
        "Avatar",
        "Frozen",
        "The Silence of the Lambs ",
        "Star Wars",
        "One Flew Over the Cuckoo's Nest"
    ],
    "Rating": [8.8, 8.4, 7.9, 8.5, 8.6, 7.8, 7.5, 8.2, 8.4, 8.1],
    "Genre": [
        "Sci-Fi",
        "Action",
        "Romance",
        "Drama",
        "Sci-Fi",
        "Fantasy",
        "Animation",
        "Thriller ",
        "Action",
        "Drama"
    ],
    "Revenue": [
        830,
        2798,
        2200,
        1074,
        701,
        2923,
        1450,
        650,
        311,
        250
    ]
}

df = pd.DataFrame(data)

print("MOVIE DATASET\n")
print(df)

print("\nHIGHEST RATED MOVIES\n")
highest_rated = df.sort_values(by="Rating", ascending=False)
print(highest_rated[["Movie_Name", "Rating"]])

print("\nMOST PROFITABLE GENRES\n")
genre_profit = df.groupby("Genre")["Revenue"].sum().sort_values(ascending=False)
print(genre_profit)

print("\nTOP 5 MOVIES BASED ON RATING\n")
top5 = df.sort_values(by="Rating", ascending=False).head(5)
print(top5[["Movie_Name", "Rating", "Revenue"]])

correlation = df["Rating"].corr(df["Revenue"])

print("\nCORRELATION BETWEEN RATING AND REVENUE\n")
print(correlation)

plt.figure(figsize=(8, 5))
genre_profit.plot(kind="bar")
plt.title("Genre vs Revenue")
plt.xlabel("Genre")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
plt.hist(df["Rating"], bins=5)
plt.title("Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
plt.scatter(df["Rating"], df["Revenue"])
plt.title("Correlation Between Rating and Revenue")
plt.xlabel("Rating")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()