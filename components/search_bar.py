import streamlit as st

def search_bar():
    """Display a search bar for movies"""
    search_query = st.text_input("Search for movies...", key="search_input")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_button = st.button("Search", use_container_width=True)
    
    with col2:
        clear_button = st.button("Clear", use_container_width=True)
    
    if clear_button:
        st.session_state.search_input = ""
        return None
    
    if search_button and search_query:
        # Add to search history
        if search_query not in st.session_state.search_history:
            st.session_state.search_history.insert(0, search_query)
            # Keep only the last 5 searches
            st.session_state.search_history = st.session_state.search_history[:5]
        
        return search_query
    
    return None