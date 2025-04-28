import streamlit as st
from api.tmdb_service import TMDbService

tmdb_service = TMDbService()

def genre_filter():
    """Display a genre filter dropdown"""
    # Fetch genres
    genres_data = tmdb_service.get_genres()
    
    if not genres_data or "genres" not in genres_data:
        st.warning("Failed to load genres.")
        return None
    
    genres = genres_data["genres"]
    genre_options = ["All Genres"] + [genre["name"] for genre in genres]
    
    selected_genre = st.selectbox("Genre", genre_options)
    
    if selected_genre == "All Genres":
        return None
    
    # Find the genre ID
    for genre in genres:
        if genre["name"] == selected_genre:
            return genre["id"]
    
    return None

def year_filter():
    """Display a year range slider"""
    import datetime
    current_year = datetime.datetime.now().year
    
    year_range = st.slider(
        "Release Year",
        min_value=1900,
        max_value=current_year,
        value=(1900, current_year)
    )
    
    return year_range

def rating_filter():
    """Display a rating range slider"""
    rating_range = st.slider(
        "Rating",
        min_value=0.0,
        max_value=10.0,
        value=(0.0, 10.0),
        step=0.5
    )
    
    return rating_range

def language_filter():
    """Display a language filter dropdown"""
    languages = [
        {"code": "en", "name": "English"},
        {"code": "es", "name": "Spanish"},
        {"code": "fr", "name": "French"},
        {"code": "de", "name": "German"},
        {"code": "it", "name": "Italian"},
        {"code": "ja", "name": "Japanese"},
        {"code": "ko", "name": "Korean"},
        {"code": "zh", "name": "Chinese"},
        {"code": "hi", "name": "Hindi"},
        {"code": "ru", "name": "Russian"}
    ]
    
    language_options = ["All Languages"] + [lang["name"] for lang in languages]
    
    selected_language = st.selectbox("Language", language_options)
    
    if selected_language == "All Languages":
        return None
    
    # Find the language code
    for lang in languages:
        if lang["name"] == selected_language:
            return lang["code"]
    
    return None

def apply_filters():
    """Display and apply all filters"""
    with st.expander("Filters"):
        col1, col2 = st.columns(2)
        
        with col1:
            genre_id = genre_filter()
            year_range = year_filter()
        
        with col2:
            rating_range = rating_filter()
            language_code = language_filter()
        
        apply_button = st.button("Apply Filters", use_container_width=True)
        
        if apply_button:
            filters = {
                "with_genres": genre_id,
                "primary_release_date.gte": f"{year_range[0]}-01-01",
                "primary_release_date.lte": f"{year_range[1]}-12-31",
                "vote_average.gte": rating_range[0],
                "vote_average.lte": rating_range[1],
                "with_original_language": language_code
            }
            
            # Remove None values
            filters = {k: v for k, v in filters.items() if v is not None}
            
            return filters
    
    return None