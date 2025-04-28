import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# TMDb API configuration
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "62c2a5b61056c6a72e2552752f2139ca")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/"
POSTER_SIZE = "w500"
BACKDROP_SIZE = "original"
PROFILE_SIZE = "w185"

# Default configuration
DEFAULT_LANGUAGE = "en-US"