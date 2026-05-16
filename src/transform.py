import json
import pandas as pd
import logging

# Logging setup
logging.basicConfig(
    filename='logs/pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def get_rating_category(rating):

    if rating >= 8:
        return "Excellent"

    elif rating >= 7:
        return "Good"

    else:
        return "Average"


def transform_movies():

    try:

        # =========================
        # LOAD RAW DATA
        # =========================

        with open(
            "data/raw/movies_raw.json",
            "r",
            encoding="utf-8"
        ) as file:

            movies = json.load(file)

        with open(
            "data/raw/cast_raw.json",
            "r",
            encoding="utf-8"
        ) as file:

            cast_data = json.load(file)

        # =========================
        # SILVER LAYER
        # =========================

        movie_list = []
        genre_list = []

        for movie in movies:

            movie_dict = {

                "movie_id": movie.get("id"),
                "title": movie.get("title"),
                "release_date": movie.get("release_date"),
                "rating": movie.get("vote_average"),
                "popularity": movie.get("popularity"),
                "vote_count": movie.get("vote_count"),
                "language": movie.get("original_language"),
                "adult": movie.get("adult"),

                # Feature engineering
                "rating_category": get_rating_category(
                    movie.get("vote_average", 0)
                )

            }

            movie_list.append(movie_dict)

            # Genre normalization
            for genre_id in movie.get("genre_ids", []):

                genre_list.append({

                    "movie_id": movie.get("id"),
                    "genre_id": genre_id

                })

        # =========================
        # CREATE DATAFRAMES
        # =========================

        movies_df = pd.DataFrame(movie_list)

        genres_df = pd.DataFrame(genre_list)

        cast_df = pd.DataFrame(cast_data)

        # =========================
        # DATA CLEANING
        # =========================

        movies_df.drop_duplicates(inplace=True)

        cast_df.drop_duplicates(inplace=True)

        genres_df.drop_duplicates(inplace=True)

        movies_df.fillna("Unknown", inplace=True)

        cast_df.fillna("Unknown", inplace=True)

        # =========================
        # SAVE SILVER LAYER
        # =========================

        movies_df.to_csv(
            "data/processed/movies_cleaned.csv",
            index=False
        )

        genres_df.to_csv(
            "data/processed/genres_cleaned.csv",
            index=False
        )

        cast_df.to_csv(
            "data/processed/cast_cleaned.csv",
            index=False
        )

        # =========================
        # GOLD LAYER
        # =========================

        # Top movies
        top_movies = movies_df.sort_values(
            by="popularity",
            ascending=False
        ).head(10)

        # Language analytics
        language_analytics = movies_df.groupby(
            "language"
        ).agg({

            "movie_id": "count",
            "rating": "mean",
            "popularity": "mean"

        }).reset_index()

        language_analytics.rename(columns={

            "movie_id": "movie_count",
            "rating": "avg_rating",
            "popularity": "avg_popularity"

        }, inplace=True)

        # Actor analytics
        actor_analytics = cast_df.groupby(
            "actor_name"
        ).agg({

            "movie_id": "count",
            "popularity": "mean"

        }).reset_index()

        actor_analytics.rename(columns={

            "movie_id": "movie_count",
            "popularity": "avg_popularity"

        }, inplace=True)

        actor_analytics = actor_analytics.sort_values(
            by="movie_count",
            ascending=False
        ).head(20)

        # Dashboard summary
        dashboard_summary = pd.DataFrame([{

            "total_movies": movies_df.shape[0],
            "average_rating": movies_df["rating"].mean(),
            "highest_popularity": movies_df["popularity"].max(),
            "top_language": movies_df["language"].mode()[0],
            "total_actors": cast_df["actor_id"].nunique()

        }])

        # =========================
        # DENORMALIZED DASHBOARD TABLE
        # =========================

        movie_dashboard = movies_df.merge(
            genres_df,
            on="movie_id",
            how="left"
        )

        # =========================
        # SAVE GOLD LAYER
        # =========================

        top_movies.to_csv(
            "data/processed/top_movies.csv",
            index=False
        )

        language_analytics.to_csv(
            "data/processed/language_analytics.csv",
            index=False
        )

        actor_analytics.to_csv(
            "data/processed/actor_analytics.csv",
            index=False
        )

        dashboard_summary.to_csv(
            "data/processed/dashboard_summary.csv",
            index=False
        )

        movie_dashboard.to_csv(
            "data/processed/movie_dashboard.csv",
            index=False
        )

        logging.info(
            "Advanced transformation completed successfully"
        )

        print("Advanced transformation successful")

    except Exception as e:

        logging.error(f"Transformation failed: {e}")

        print(f"Transformation failed: {e}")


if __name__ == "__main__":

    transform_movies()