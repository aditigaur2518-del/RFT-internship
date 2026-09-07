import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt
from collections import Counter


st.set_page_config(
    page_title="Social Media Trend Analyzer",
    page_icon="📱",
    layout="wide"
)


# --------------------------------------------------
# SENTIMENT ANALYSIS
# --------------------------------------------------

positive_words = {
    "good", "great", "excellent", "amazing", "awesome",
    "happy", "love", "loved", "best", "beautiful",
    "fantastic", "wonderful", "success", "successful",
    "enjoy", "enjoyed", "like", "liked", "win", "winning",
    "positive", "fun", "excited", "cool"
}

negative_words = {
    "bad", "worst", "terrible", "awful", "sad",
    "hate", "hated", "poor", "angry", "fail",
    "failed", "failure", "negative", "boring",
    "disappointed", "disappointing", "problem",
    "problems", "issue", "issues", "loss", "losing"
}


def analyze_sentiment(text):

    text = str(text).lower()

    words = re.findall(r"\b[a-zA-Z]+\b", text)

    positive_count = sum(
        1 for word in words
        if word in positive_words
    )

    negative_count = sum(
        1 for word in words
        if word in negative_words
    )

    if positive_count > negative_count:
        return "Positive"

    elif negative_count > positive_count:
        return "Negative"

    else:
        return "Neutral"


# --------------------------------------------------
# HASHTAG EXTRACTION
# --------------------------------------------------

def extract_hashtags(text):

    hashtags = re.findall(
        r"#\w+",
        str(text).lower()
    )

    return hashtags


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

def prepare_data(df):

    required_columns = [
        "Date",
        "User",
        "Post",
        "Likes",
        "Comments",
        "Shares",
        "Category"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        st.error(
            "Missing columns: "
            + ", ".join(missing_columns)
        )

        st.stop()

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    df["Likes"] = pd.to_numeric(
        df["Likes"],
        errors="coerce"
    ).fillna(0)

    df["Comments"] = pd.to_numeric(
        df["Comments"],
        errors="coerce"
    ).fillna(0)

    df["Shares"] = pd.to_numeric(
        df["Shares"],
        errors="coerce"
    ).fillna(0)

    df["Engagement"] = (
        df["Likes"]
        + df["Comments"]
        + df["Shares"]
    )

    df["Sentiment"] = df["Post"].apply(
        analyze_sentiment
    )

    df["Hashtags"] = df["Post"].apply(
        extract_hashtags
    )

    df["Posting Time"] = df["Date"].dt.hour

    df["Posting Hour"] = df["Posting Time"].apply(
        lambda x: f"{int(x):02d}:00"
        if pd.notna(x)
        else "Unknown"
    )

    return df


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title(" Dashboard Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload Social Media CSV",
    type=["csv"]
)


# --------------------------------------------------
# LOAD CSV
# --------------------------------------------------

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

else:

    try:

        df = pd.read_csv(
            "social_media_data.csv"
        )

    except FileNotFoundError:

        st.warning(
            "Please upload a CSV file "
            "or create social_media_data.csv."
        )

        st.stop()


df = prepare_data(df)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title(
    "Social Media Trend Analyzer"
)

st.write(
    "Analyze hashtags, users, engagement, "
    "posting time, content categories and sentiment."
)


# --------------------------------------------------
# SEARCH
# --------------------------------------------------

st.sidebar.subheader("Search")

search_text = st.sidebar.text_input(
    "Search posts, users or hashtags"
)


# --------------------------------------------------
# FILTERS
# --------------------------------------------------

st.sidebar.subheader(" Filters")

categories = sorted(
    df["Category"].dropna().unique()
)

selected_categories = st.sidebar.multiselect(
    "Content Category",
    categories,
    default=categories
)

sentiments = [
    "Positive",
    "Neutral",
    "Negative"
]

selected_sentiments = st.sidebar.multiselect(
    "Sentiment",
    sentiments,
    default=sentiments
)

users = sorted(
    df["User"].dropna().unique()
)

selected_users = st.sidebar.multiselect(
    "Users",
    users,
    default=users
)


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = df[
    df["Category"].isin(
        selected_categories
    )
]

filtered_df = filtered_df[
    filtered_df["Sentiment"].isin(
        selected_sentiments
    )
]

filtered_df = filtered_df[
    filtered_df["User"].isin(
        selected_users
    )
]


if search_text:

    search_lower = search_text.lower()

    filtered_df = filtered_df[
        filtered_df["Post"]
        .astype(str)
        .str.lower()
        .str.contains(
            search_lower,
            na=False
        )
        |
        filtered_df["User"]
        .astype(str)
        .str.lower()
        .str.contains(
            search_lower,
            na=False
        )
    ]


# --------------------------------------------------
# DASHBOARD METRICS
# --------------------------------------------------

st.subheader(" Overall Analytics")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Posts",
        len(filtered_df)
    )

with col2:

    st.metric(
        "Total Likes",
        int(filtered_df["Likes"].sum())
    )

with col3:

    st.metric(
        "Total Comments",
        int(filtered_df["Comments"].sum())
    )

with col4:

    st.metric(
        "Total Engagement",
        int(filtered_df["Engagement"].sum())
    )


# --------------------------------------------------
# HASHTAG ANALYSIS
# --------------------------------------------------

st.subheader(" Top Trending Hashtags")

hashtag_counter = Counter()

for hashtags in filtered_df["Hashtags"]:

    hashtag_counter.update(hashtags)


top_hashtags = hashtag_counter.most_common(10)


if top_hashtags:

    hashtag_df = pd.DataFrame(
        top_hashtags,
        columns=[
            "Hashtag",
            "Count"
        ]
    )

    st.dataframe(
        hashtag_df,
        use_container_width=True
    )

    fig, ax = plt.subplots()

    ax.bar(
        hashtag_df["Hashtag"],
        hashtag_df["Count"]
    )

    ax.set_title(
        "Top Trending Hashtags"
    )

    ax.set_xlabel("Hashtag")

    ax.set_ylabel("Number of Posts")

    plt.xticks(rotation=45)

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)

else:

    st.info(
        "No hashtags found."
    )


# --------------------------------------------------
# MOST ACTIVE USERS
# --------------------------------------------------

st.subheader("👥 Most Active Users")

active_users = (
    filtered_df["User"]
    .value_counts()
    .head(10)
    .reset_index()
)

active_users.columns = [
    "User",
    "Post Count"
]

st.dataframe(
    active_users,
    use_container_width=True
)


# --------------------------------------------------
# ENGAGEMENT ANALYSIS
# --------------------------------------------------

st.subheader(" Engagement Analysis")

engagement_summary = pd.DataFrame({
    "Metric": [
        "Likes",
        "Comments",
        "Shares"
    ],
    "Total": [
        filtered_df["Likes"].sum(),
        filtered_df["Comments"].sum(),
        filtered_df["Shares"].sum()
    ]
})

st.dataframe(
    engagement_summary,
    use_container_width=True
)


# --------------------------------------------------
# DAILY ENGAGEMENT TREND
# --------------------------------------------------

st.subheader("Daily Engagement Trend")

daily_engagement = (
    filtered_df
    .groupby(
        filtered_df["Date"].dt.date
    )["Engagement"]
    .sum()
    .reset_index()
)

daily_engagement.columns = [
    "Date",
    "Engagement"
]

if not daily_engagement.empty:

    fig, ax = plt.subplots()

    ax.plot(
        daily_engagement["Date"],
        daily_engagement["Engagement"],
        marker="o"
    )

    ax.set_title(
        "Daily Engagement Trend"
    )

    ax.set_xlabel("Date")

    ax.set_ylabel("Engagement")

    plt.xticks(rotation=45)

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# --------------------------------------------------
# CONTENT CATEGORY DISTRIBUTION
# --------------------------------------------------

st.subheader(
    "Content Category Distribution"
)

category_counts = (
    filtered_df["Category"]
    .value_counts()
)

if not category_counts.empty:

    fig, ax = plt.subplots()

    ax.pie(
        category_counts.values,
        labels=category_counts.index,
        autopct="%1.1f%%"
    )

    ax.set_title(
        "Content Category Distribution"
    )

    st.pyplot(fig)

    plt.close(fig)


# --------------------------------------------------
# POPULAR POSTING TIME
# --------------------------------------------------

st.subheader(
    "Most Popular Posting Time"
)

posting_times = (
    filtered_df["Posting Hour"]
    .value_counts()
)

if not posting_times.empty:

    popular_time = posting_times.idxmax()

    popular_count = posting_times.max()

    st.success(
        f"Most popular posting time: "
        f"**{popular_time}** "
        f"({popular_count} posts)"
    )

    posting_df = (
        posting_times
        .reset_index()
    )

    posting_df.columns = [
        "Posting Time",
        "Post Count"
    ]

    st.dataframe(
        posting_df,
        use_container_width=True
    )


# --------------------------------------------------
# SENTIMENT ANALYSIS
# --------------------------------------------------

st.subheader(
    " Sentiment Analysis"
)

sentiment_counts = (
    filtered_df["Sentiment"]
    .value_counts()
)

sentiment_df = (
    sentiment_counts
    .reset_index()
)

sentiment_df.columns = [
    "Sentiment",
    "Post Count"
]

st.dataframe(
    sentiment_df,
    use_container_width=True
)

if not sentiment_counts.empty:

    fig, ax = plt.subplots()

    ax.bar(
        sentiment_counts.index,
        sentiment_counts.values
    )

    ax.set_title(
        "Sentiment Distribution"
    )

    ax.set_xlabel("Sentiment")

    ax.set_ylabel("Number of Posts")

    st.pyplot(fig)

    plt.close(fig)


# --------------------------------------------------
# FILTERED POSTS
# --------------------------------------------------

st.subheader(
    " Filtered Social Media Posts"
)

display_columns = [
    "Date",
    "User",
    "Post",
    "Category",
    "Likes",
    "Comments",
    "Shares",
    "Engagement",
    "Sentiment",
    "Posting Hour"
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True
)


# --------------------------------------------------
# EXPORT ANALYTICS REPORT
# --------------------------------------------------

st.subheader(
    "Export Analytics Report"
)

report = filtered_df[display_columns].copy()

csv_data = report.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Analytics Report",
    data=csv_data,
    file_name="social_media_analytics_report.csv",
    mime="text/csv"
)


# --------------------------------------------------
# FINAL SUMMARY
# --------------------------------------------------

st.subheader(" Key Insights")

if not filtered_df.empty:

    top_user = (
        filtered_df["User"]
        .value_counts()
        .idxmax()
    )

    top_category = (
        filtered_df["Category"]
        .value_counts()
        .idxmax()
    )

    top_sentiment = (
        filtered_df["Sentiment"]
        .value_counts()
        .idxmax()
    )

    st.write(
        f"👤 **Most Active User:** {top_user}"
    )

    if top_hashtags:

        st.write(
            f" **Top Hashtag:** "
            f"{top_hashtags[0][0]}"
        )

    st.write(
        f" **Most Popular Category:** "
        f"{top_category}"
    )

    st.write(
        f" **Overall Dominant Sentiment:** "
        f"{top_sentiment}"
    )

    st.write(
        f" **Total Engagement:** "
        f"{int(filtered_df['Engagement'].sum())}"
    )

else:

    st.info(
        "No posts match the selected filters."
    )