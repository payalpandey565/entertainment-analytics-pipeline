import pandas as pd
import logging

# Logging setup
logging.basicConfig(
    filename='logs/pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def validate_and_load():

    try:

        # =========================
        # LOAD GOLD/SILVER DATASETS
        # =========================

        movies_df = pd.read_csv(
            "data/processed/movies_cleaned.csv"
        )

        genres_df = pd.read_csv(
            "data/processed/genres_cleaned.csv"
        )

        cast_df = pd.read_csv(
            "data/processed/cast_cleaned.csv"
        )

        # =========================
        # DATA QUALITY CHECKS
        # =========================

        quality_checks = []

        # Null checks
        movie_nulls = movies_df.isnull().sum().sum()

        cast_nulls = cast_df.isnull().sum().sum()

        # Duplicate checks
        movie_duplicates = movies_df.duplicated().sum()

        cast_duplicates = cast_df.duplicated().sum()

        # Business rule checks
        invalid_ratings = movies_df[
            (movies_df["rating"] < 0) |
            (movies_df["rating"] > 10)
        ].shape[0]

        negative_popularity = movies_df[
            movies_df["popularity"] < 0
        ].shape[0]

        missing_actor_names = cast_df[
            cast_df["actor_name"] == "Unknown"
        ].shape[0]

        # =========================
        # CREATE QUALITY REPORT
        # =========================

        quality_checks.append({

            "check": "movie_nulls",
            "count": movie_nulls

        })

        quality_checks.append({

            "check": "cast_nulls",
            "count": cast_nulls

        })

        quality_checks.append({

            "check": "movie_duplicates",
            "count": movie_duplicates

        })

        quality_checks.append({

            "check": "cast_duplicates",
            "count": cast_duplicates

        })

        quality_checks.append({

            "check": "invalid_ratings",
            "count": invalid_ratings

        })

        quality_checks.append({

            "check": "negative_popularity",
            "count": negative_popularity

        })

        quality_checks.append({

            "check": "missing_actor_names",
            "count": missing_actor_names

        })

        quality_df = pd.DataFrame(quality_checks)

        # =========================
        # PIPELINE METRICS
        # =========================

        pipeline_metrics = pd.DataFrame([{

            "total_movies": movies_df.shape[0],
            "total_genres": genres_df.shape[0],
            "total_cast_records": cast_df.shape[0],
            "unique_actors": cast_df["actor_id"].nunique()

        }])

        # =========================
        # SAVE REPORTS
        # =========================

        quality_df.to_csv(
            "data/processed/data_quality_report.csv",
            index=False
        )

        pipeline_metrics.to_csv(
            "data/processed/pipeline_metrics.csv",
            index=False
        )

        logging.info(
            "Load validation completed successfully"
        )

        print("\nLoad layer completed successfully")

        print("\nPipeline Metrics:")
        print(pipeline_metrics)

        print("\nData Quality Report:")
        print(quality_df)

    except Exception as e:

        logging.error(f"Load layer failed: {e}")

        print(f"Load layer failed: {e}")


if __name__ == "__main__":

    validate_and_load()