import streamlit as st
import time

def format_runtime(minutes):
    """Format runtime from minutes to hours and minutes"""
    if not minutes:
        return "N/A"
    
    hours = minutes // 60
    mins = minutes % 60
    
    if hours > 0:
        return f"{hours}h {mins}m"
    return f"{mins}m"

def format_date(date_str):
    """Format date string to a more readable format"""
    if not date_str:
        return "N/A"
    
    try:
        from datetime import datetime
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%B %d, %Y")
    except:
        return date_str

def get_youtube_embed_url(video_key):
    """Get YouTube embed URL from video key"""
    if not video_key:
        return None
    
    return f"https://www.youtube.com/embed/{video_key}"

def load_with_spinner(func, *args, **kwargs):
    """Execute a function with a spinner"""
    with st.spinner("Loading..."):
        return func(*args, **kwargs)

def get_trailer_key(videos):
    """Get the key of the official trailer from videos list"""
    if not videos or "results" not in videos:
        return None
    
    # First, try to find the official trailer
    for video in videos["results"]:
        if video["type"].lower() == "trailer" and "official" in video["name"].lower():
            return video["key"]
    
    # If no official trailer, get any trailer
    for video in videos["results"]:
        if video["type"].lower() == "trailer":
            return video["key"]
    
    # If no trailer at all, get any video
    if videos["results"]:
        return videos["results"][0]["key"]
    
    return None

def init_session_state():
    """Initialize session state variables"""
    if "favorites" not in st.session_state:
        st.session_state.favorites = []
    
    if "search_history" not in st.session_state:
        st.session_state.search_history = []
    
    if "current_page" not in st.session_state:
        st.session_state.current_page = 1
        
    if "selected_movie" not in st.session_state:
        st.session_state.selected_movie = None