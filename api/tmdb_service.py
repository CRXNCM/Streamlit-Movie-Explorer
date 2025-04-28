import requests
from .config import TMDB_API_KEY, TMDB_BASE_URL, TMDB_IMAGE_BASE_URL, POSTER_SIZE, BACKDROP_SIZE, DEFAULT_LANGUAGE

class TMDbService:
    def __init__(self):
        self.api_key = TMDB_API_KEY
        self.base_url = TMDB_BASE_URL
        self.image_base_url = TMDB_IMAGE_BASE_URL
        
    def _make_request(self, endpoint, params=None):
        """Make a request to the TMDb API"""
        if params is None:
            params = {}
        
        params["api_key"] = self.api_key
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")
            return None
    
    def get_trending_movies(self, time_window="week", page=1):
        """Get trending movies for the day or week"""
        endpoint = f"trending/movie/{time_window}"
        params = {
            "language": DEFAULT_LANGUAGE,
            "page": page
        }
        return self._make_request(endpoint, params)
    
    def search_movies(self, query, page=1, include_adult=False):
        """Search for movies by title"""
        endpoint = "search/movie"
        params = {
            "query": query,
            "language": DEFAULT_LANGUAGE,
            "page": page,
            "include_adult": include_adult
        }
        return self._make_request(endpoint, params)
    
    def get_movie_details(self, movie_id):
        """Get detailed information about a movie"""
        endpoint = f"movie/{movie_id}"
        params = {
            "language": DEFAULT_LANGUAGE,
            "append_to_response": "credits,videos,recommendations,similar"
        }
        return self._make_request(endpoint, params)
    
    def get_movie_poster_url(self, poster_path, size=POSTER_SIZE):
        """Get the full URL for a movie poster"""
        if not poster_path:
            return None
        return f"{self.image_base_url}{size}{poster_path}"
    
    def get_backdrop_url(self, backdrop_path, size=BACKDROP_SIZE):
        """Get the full URL for a movie backdrop"""
        if not backdrop_path:
            return None
        return f"{self.image_base_url}{size}{backdrop_path}"
    
    def get_profile_url(self, profile_path, size=POSTER_SIZE):
        """Get the full URL for a person's profile image"""
        if not profile_path:
            return None
        return f"{self.image_base_url}{size}{profile_path}"
    
    def get_genres(self):
        """Get the list of official genres for movies"""
        endpoint = "genre/movie/list"
        params = {
            "language": DEFAULT_LANGUAGE
        }
        return self._make_request(endpoint, params)
    
    def discover_movies(self, params=None):
        """Discover movies by different types of data"""
        endpoint = "discover/movie"
        return self._make_request(endpoint, params)