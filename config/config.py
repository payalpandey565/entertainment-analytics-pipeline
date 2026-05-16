from dotenv import load_dotenv
import os

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")