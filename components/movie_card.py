import streamlit as st
from api.tmdb_service import TMDbService
from utils.helpers import format_runtime, format_date, get_trailer_key, get_youtube_embed_url

tmdb_service = TMDbService()

def movie_card(movie, expanded=False):
    """Display a movie card with basic information"""
    poster_url = tmdb_service.get_movie_poster_url(movie.get("poster_path"))
    
    col1, col2 = st.columns([1, 3])
    
    # In the movie_card function where st.image is used with use_column_width
    with col1:
        if poster_url:
            st.image(poster_url, use_container_width=True)
        else:
            st.image("https://via.placeholder.com/500x750?text=No+Image", use_container_width=True)
    
    with col2:
        title = movie.get("title", "Unknown Title")
        year = movie.get("release_date", "")[:4] if movie.get("release_date") else "Unknown Year"
        
        st.markdown(f"## {title} ({year})")
        
        # Rating
        vote_average = movie.get("vote_average", 0)
        st.markdown(f"**Rating:** ⭐ {vote_average:.1f}/10")
        
        # Overview
        overview = movie.get("overview", "No overview available.")
        st.markdown(f"**Overview:** {overview}")
        
        # Add to favorites button
        if st.button("❤️ Add to Favorites", key=f"fav_{movie.get('id')}"):
            if movie not in st.session_state.favorites:
                st.session_state.favorites.append(movie)
                st.success(f"Added {title} to favorites!")
            else:
                st.warning(f"{title} is already in your favorites!")
    
    # Expandable section for more details
    if expanded:
        st.markdown("---")
        display_movie_details(movie)

def display_movie_details(movie_id):
    """Display detailed information about a movie"""
    # If movie_id is a dictionary (full movie object), extract the ID
    if isinstance(movie_id, dict):
        movie_id = movie_id.get("id")
    
    # Fetch detailed movie information
    movie = tmdb_service.get_movie_details(movie_id)
    
    if not movie:
        st.error("Failed to load movie details.")
        return
    
    # Basic information
    st.markdown("### Movie  Details")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**Release Date:** {format_date(movie.get('release_date'))}")
    
    with col2:
        st.markdown(f"**Runtime:** {format_runtime(movie.get('runtime'))}")
    
    with col3:
        st.markdown(f"**Status:** {movie.get('status', 'N/A')}")
    
    # Genres
    genres = ", ".join([genre["name"] for genre in movie.get("genres", [])])
    st.markdown(f"**Genres:** {genres if genres else 'N/A'}")
    
    # Cast
    st.markdown("### Top Cast")
    cast_cols = st.columns(4)
    
    cast = movie.get("credits", {}).get("cast", [])
    for i, actor in enumerate(cast[:4]):
        with cast_cols[i]:
            profile_url = tmdb_service.get_profile_url(actor.get("profile_path"))
            if profile_url:
                st.image(profile_url, width=150)
            else:
                st.image("https://via.placeholder.com/150x225?text=No+Image", width=150)
            st.markdown(f"**{actor.get('name')}**")
            st.markdown(f"as {actor.get('character')}")
    
    # Trailer
    st.markdown("### Trailer")
    videos = movie.get("videos", {})
    trailer_key = get_trailer_key(videos)
    
    if trailer_key:
        trailer_url = get_youtube_embed_url(trailer_key)
        st.video(trailer_url)
    else:
        st.info("No trailer available for this movie.")
    
    # Similar Movies
    st.markdown("### Similar Movies")
    similar_movies = movie.get("similar", {}).get("results", [])
    
    if similar_movies:
        similar_cols = st.columns(4)
        # In the display_movie_details function where similar movies are displayed
        for i, similar_movie in enumerate(similar_movies[:4]):
            with similar_cols[i]:
                poster_url = tmdb_service.get_movie_poster_url(similar_movie.get("poster_path"))
                if poster_url:
                    st.image(poster_url, use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/500x750?text=No+Image", use_container_width=True)
                st.markdown(f"**{similar_movie.get('title')}**")
                st.markdown(f"{similar_movie.get('release_date', '')[:4] if similar_movie.get('release_date') else ''}")
                
                if st.button("View Details", key=f"similar_{similar_movie.get('id')}"):
                    st.session_state.selected_movie = similar_movie.get('id')
                    # Replace this line
                    st.experimental_rerun()
                    
                    # With this
                    st.rerun()
    else:
        st.info("No similar movies found.")