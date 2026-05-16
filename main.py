from src.extract import fetch_movies, fetch_cast
from src.transform import transform_movies
from src.load import validate_and_load


def run_pipeline():

    print("\nStarting Entertainment Analytics Pipeline...\n")

    # =========================
    # EXTRACTION LAYER
    # =========================

    print("Running extraction layer...\n")

    movies = fetch_movies()

    fetch_cast(movies)

    # =========================
    # TRANSFORMATION LAYER
    # =========================

    print("\nRunning transformation layer...\n")

    transform_movies()

    # =========================
    # LOAD + VALIDATION LAYER
    # =========================

    print("\nRunning load and validation layer...\n")

    validate_and_load()

    print("\nPipeline executed successfully!\n")


if __name__ == "__main__":

    run_pipeline()