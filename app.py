import streamlit as st
import os
from api.tmdb_service import TMDbService
from components.movie_card import movie_card, display_movie_details
from components.search_bar import search_bar
from components.filters import apply_filters
from utils.helpers import init_session_state, load_with_spinner

# Initialize TMDb service
tmdb_service = TMDbService()

# Page configuration
st.set_page_config(
    page_title="Movie Explorer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css_file = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
    with open(css_file, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
init_session_state()

# Load CSS
load_css()

# Sidebar
with st.sidebar:
    st.title("🎬 Movie Explorer")
    
    # Navigation
    page = st.radio("Navigation", ["Home", "Search", "Favorites"])
    
    # API Key input
    if not tmdb_service.api_key:
        st.warning("TMDb API key not found. Please enter your API key below.")
        api_key = st.text_input("TMDb API Key", type="password")
        if api_key:
            tmdb_service.api_key = api_key
            st.success("API key set successfully!")
    
    # Search history
    if st.session_state.search_history:
        st.subheader("Recent Searches")
        for query in st.session_state.search_history:
            if st.button(query, key=f"history_{query}"):
                st.session_state.search_input = query
                page = "Search"
    
    # About section
    st.markdown("---")
    st.markdown("### About")
    st.markdown("Movie Explorer is a Streamlit app that allows you to search for movies and get detailed information.")
    st.markdown("Data provided by [TMDb](https://www.themoviedb.org/).")

# Main content
if page == "Home":
    st.title("Trending Movies")
    
    # Time window selector
    time_window = st.radio("Trending in:", ["Today", "This Week"], horizontal=True)
    time_window_value = "day" if time_window == "Today" else "week"
    
    # Fetch trending movies
    trending_movies = load_with_spinner(
        tmdb_service.get_trending_movies,
        time_window=time_window_value,
        page=st.session_state.current_page
    )
    
    if not trending_movies or "results" not in trending_movies:
        st.error("Failed to load trending movies. Please check your API key.")
    else:
        # Display movies in a grid
        movies = trending_movies["results"]
        
        # Create rows with 4 movies each
        # In the Home section where trending movies are displayed
        for i in range(0, len(movies), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(movies):
                    with cols[j]:
                        movie = movies[i + j]
                        poster_url = tmdb_service.get_movie_poster_url(movie.get("poster_path"))
                        
                        if poster_url:
                            st.image(poster_url, use_container_width=True)
                        else:
                            st.image("https://via.placeholder.com/500x750?text=No+Image", use_container_width=True)
                        
                        st.markdown(f"**{movie.get('title')}**")
                        st.markdown(f"⭐ {movie.get('vote_average', 0):.1f}/10")
                        
                        # In the trending movies section where you have the View Details button
                        if st.button("View Details", key=f"trending_{movie.get('id')}"):
                            st.session_state.selected_movie = movie.get('id')
                            # Replace experimental_rerun with rerun
                            st.rerun()
        
        # Pagination
        total_pages = trending_movies.get("total_pages", 1)
        
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            if st.session_state.current_page > 1:
                if st.button("Previous Page"):
                    st.session_state.current_page -= 1
                    st.rerun()
        
        with col2:
            st.markdown(f"<div style='text-align: center;'>Page {st.session_state.current_page} of {min(total_pages, 500)}</div>", unsafe_allow_html=True)
        
        with col3:
            if st.session_state.current_page < min(total_pages, 500):
                if st.button("Next Page"):
                    st.session_state.current_page += 1
                    st.rerun()

elif page == "Search":
    st.title("Search Movies")
    
    # Search bar
    query = search_bar()
    
    # Filters
    filters = apply_filters()
    
    # If search query is provided, search for movies
    if query:
        search_results = load_with_spinner(
            tmdb_service.search_movies,
            query=query,
            page=st.session_state.current_page
        )
        
        if not search_results or "results" not in search_results:
            st.error("Failed to load search results.")
        elif not search_results["results"]:
            st.info(f"No results found for '{query}'.")
        else:
            st.subheader(f"Search Results for '{query}'")
            
            # Display movies
            movies = search_results["results"]
            
            for movie in movies:
                movie_card(movie)
                st.markdown("---")
            
            # Pagination
            total_pages = search_results.get("total_pages", 1)
            
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col1:
                if st.session_state.current_page > 1:
                    if st.button("Previous Page"):
                        st.session_state.current_page -= 1
                        st.rerun()
            
            with col2:
                st.markdown(f"<div style='text-align: center;'>Page {st.session_state.current_page} of {min(total_pages, 500)}</div>", unsafe_allow_html=True)
            
            with col3:
                if st.session_state.current_page < min(total_pages, 500):
                    if st.button("Next Page"):
                        st.session_state.current_page += 1
                        st.rerun()
    
    # If filters are applied but no search query, use discover
    elif filters:
        discover_results = load_with_spinner(
            tmdb_service.discover_movies,
            params={**filters, "page": st.session_state.current_page}
        )
        
        if not discover_results or "results" not in discover_results:
            st.error("Failed to load movies with the selected filters.")
        elif not discover_results["results"]:
            st.info("No movies found with the selected filters.")
        else:
            st.subheader("Movies matching your filters")
            
            # Display movies
            movies = discover_results["results"]
            
            for movie in movies:
                movie_card(movie)
                st.markdown("---")
            
            # Pagination
            total_pages = discover_results.get("total_pages", 1)
            
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col1:
                if st.session_state.current_page > 1:
                    if st.button("Previous Page"):
                        st.session_state.current_page -= 1
                        st.rerun()
            
            with col2:
                st.markdown(f"<div style='text-align: center;'>Page {st.session_state.current_page} of {min(total_pages, 500)}</div>", unsafe_allow_html=True)
            
            with col3:
                if st.session_state.current_page < min(total_pages, 500):
                    if st.button("Next Page"):
                        st.session_state.current_page += 1
                        st.rerun()

elif page == "Favorites":
    st.title("Your Favorites")
    
    if not st.session_state.favorites:
        st.info("You haven't added any movies to your favorites yet.")
    else:
        # Add a clear all button
        if st.button("Clear All Favorites"):
            st.session_state.favorites = []
            st.success("Favorites cleared!")
            st.rerun()
        
        # Display favorite movies
        for movie in st.session_state.favorites:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                movie_card(movie)
            
            with col2:
                if st.button("View Details", key=f"fav_details_{movie.get('id')}"):
                    st.session_state.selected_movie = movie.get('id')
            
            with col3:
                if st.button("Remove", key=f"remove_{movie.get('id')}"):
                    st.session_state.favorites.remove(movie)
                    st.success(f"Removed {movie.get('title')} from favorites!")
                    st.rerun()
            
            st.markdown("---")

# Check if a movie is selected for detailed view
if "selected_movie" in st.session_state and st.session_state.selected_movie:
    # Create a modal-like effect
    st.markdown("---")
    st.subheader("Movie Details")
    
    # Display movie details
    display_movie_details(st.session_state.selected_movie)
    
    # Close button
    if st.button("Close Details"):
        st.session_state.selected_movie = None
        st.rerun()