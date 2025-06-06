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
    
    # Create a container with custom styling for a modal-like effect
    modal_container = st.container()
    
    with modal_container:
        # Add styling for modal but with simpler approach
        st.markdown("""
        <style>
        .movie-modal {
            background-color: rgb(17, 23, 33);
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
            border: 1px solid rgba(250, 250, 250, 0.2);
            box-shadow: 0 8px 40px rgba(0, 0, 0, 0.4);
        }
        .modal-section {
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create a more Streamlit-friendly modal
        st.markdown('<div class="movie-modal">', unsafe_allow_html=True)
        
        # Header with movie title and close button
        col1, col2 = st.columns([5, 1])
        with col1:
            title = movie.get("title", "Unknown Title")
            year = movie.get("release_date", "")[:4] if movie.get("release_date") else "Unknown Year"
            st.markdown(f"## {title} ({year})")
        
        with col2:
            if st.button("✖️ Close", key=f"close_modal_{movie_id}"):
                st.session_state.selected_movie = None
                st.rerun()
        
        # Movie poster and basic info
        col1, col2 = st.columns([1, 3])
        
        with col1:
            poster_url = tmdb_service.get_movie_poster_url(movie.get("poster_path"))
            if poster_url:
                st.image(poster_url, use_container_width=True)
            else:
                st.image("https://via.placeholder.com/500x750?text=No+Image", use_container_width=True)
        
        with col2:
            # Basic information
            st.markdown("### Movie Details")
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.markdown(f"**Release Date:** {format_date(movie.get('release_date'))}")
            
            with col_b:
                st.markdown(f"**Runtime:** {format_runtime(movie.get('runtime'))}")
            
            with col_c:
                st.markdown(f"**Status:** {movie.get('status', 'N/A')}")
            
            # Genres
            genres = ", ".join([genre["name"] for genre in movie.get("genres", [])])
            st.markdown(f"**Genres:** {genres if genres else 'N/A'}")
            
            # Rating
            vote_average = movie.get("vote_average", 0)
            st.markdown(f"**Rating:** ⭐ {vote_average:.1f}/10")
            
            # Overview
            overview = movie.get("overview", "No overview available.")
            st.markdown(f"**Overview:** {overview}")
            
            # Add to favorites button
            if st.button("❤️ Add to Favorites", key=f"modal_fav_{movie_id}"):
                if movie not in st.session_state.favorites:
                    st.session_state.favorites.append(movie)
                    st.success(f"Added {title} to favorites!")
                else:
                    st.warning(f"{title} is already in your favorites!")
        
        st.markdown('<hr class="modal-section">', unsafe_allow_html=True)
        
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
        
        st.markdown('<hr class="modal-section">', unsafe_allow_html=True)
        
        # Trailer
        st.markdown("### Trailer")
        videos = movie.get("videos", {})
        trailer_key = get_trailer_key(videos)
        
        if trailer_key:
            trailer_url = get_youtube_embed_url(trailer_key)
            st.video(trailer_url)
        else:
            st.info("No trailer available for this movie.")
        
        st.markdown('<hr class="modal-section">', unsafe_allow_html=True)
        
        # Similar Movies
        st.markdown("### Similar Movies")
        similar_movies = movie.get("similar", {}).get("results", [])
        
        if similar_movies:
            similar_cols = st.columns(4)
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
                        st.rerun()
        else:
            st.info("No similar movies found.")
        
        st.markdown('</div>', unsafe_allow_html=True)