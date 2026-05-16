import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Entertainment Analytics Dashboard",
    layout="wide"
)

st.title("🎬 Entertainment Analytics Dashboard")

# =========================
# LOAD DATA
# =========================

summary_df = pd.read_csv(
    "data/processed/dashboard_summary.csv"
)

top_movies_df = pd.read_csv(
    "data/processed/top_movies.csv"
)

actor_df = pd.read_csv(
    "data/processed/actor_analytics.csv"
)

language_df = pd.read_csv(
    "data/processed/language_analytics.csv"
)

movies_df = pd.read_csv(
    "data/processed/movies_cleaned.csv"
)

# =========================
# FIX INDEXING
# =========================

top_movies_df.index = range(1, len(top_movies_df) + 1)

movies_df.index = range(1, len(movies_df) + 1)

# =========================
# KPI SECTION
# =========================

st.header("📊 Pipeline KPIs")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Movies",
    int(summary_df["total_movies"][0])
)

col2.metric(
    "Average Rating",
    round(summary_df["average_rating"][0], 2)
)

col3.metric(
    "Highest Popularity",
    round(summary_df["highest_popularity"][0], 2)
)

col4.metric(
    "Total Actors",
    int(summary_df["total_actors"][0])
)

# =========================
# TOP MOVIES
# =========================

st.header("🔥 Top 10 Popular Movies")

st.dataframe(top_movies_df)

# =========================
# ACTOR ANALYTICS
# =========================

st.header("🎭 Top Actors by Movie Count")

st.bar_chart(
    actor_df.set_index("actor_name")["movie_count"]
)

# =========================
# LANGUAGE ANALYTICS
# =========================

st.header("🌍 Language Distribution")

st.bar_chart(
    language_df.set_index("language")["movie_count"]
)

# =========================
# RATING CATEGORY ANALYTICS
# =========================

st.header("⭐ Rating Category Distribution")

rating_counts = movies_df[
    "rating_category"
].value_counts()

st.bar_chart(rating_counts)

# =========================
# MOVIE DATA TABLE
# =========================

st.header("🎥 Complete Movie Dataset")

st.dataframe(movies_df)