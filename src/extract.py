import requests
import json
import logging

from config.config import TMDB_ACCESS_TOKEN

# Logging setup
logging.basicConfig(
    filename='logs/pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Base URL
BASE_URL = "https://api.themoviedb.org/3"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"
}


def fetch_movies():

    all_movies = []

    try:

        # Fetch multiple pages
        for page in range(1, 6):

            url = f"{BASE_URL}/movie/popular?page={page}"

            response = requests.get(url, headers=headers)

            if response.status_code == 200:

                data = response.json()

                movies = data.get("results", [])

                all_movies.extend(movies)

                logging.info(f"Page {page} extracted successfully")

                print(f"Fetched page {page}")

            else:

                logging.error(
                    f"Movie API failed for page {page}: {response.text}"
                )

        # Save movie raw data
        with open(
            "data/raw/movies_raw.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(all_movies, file, indent=4)

        logging.info("All movie data extracted successfully")

        print("\nMovie extraction completed")

        return all_movies

    except Exception as e:

        logging.error(f"Movie extraction failed: {e}")

        return []


def fetch_cast(movies):

    cast_data = []

    try:

        for movie in movies:

            movie_id = movie.get("id")

            credits_url = f"{BASE_URL}/movie/{movie_id}/credits"

            response = requests.get(
                credits_url,
                headers=headers
            )

            if response.status_code == 200:

                credits = response.json()

                cast_list = credits.get("cast", [])

                # Limit top 5 cast members
                for actor in cast_list[:5]:

                    cast_data.append({

                        "movie_id": movie_id,
                        "actor_id": actor.get("id"),
                        "actor_name": actor.get("name"),
                        "character": actor.get("character"),
                        "popularity": actor.get("popularity")

                    })

                logging.info(
                    f"Cast extracted for movie {movie_id}"
                )

            else:

                logging.error(
                    f"Credits API failed for movie {movie_id}"
                )

        # Save cast raw data
        with open(
            "data/raw/cast_raw.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(cast_data, file, indent=4)

        logging.info("All cast data extracted successfully")

        print("Cast extraction completed")

    except Exception as e:

        logging.error(f"Cast extraction failed: {e}")


if __name__ == "__main__":

    movies = fetch_movies()

    fetch_cast(movies)