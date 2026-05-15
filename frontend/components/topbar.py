import streamlit as st

from utils.theme import get_theme, set_theme


def render_topbar(show_refresh: bool = True):
    st.markdown("""
    <style>
    /* Styling for topbar buttons by targeting the first set of columns in the main area */
    [data-testid="stMainBlockContainer"] > div:first-child [data-testid="stButton"] button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: var(--text-color) !important;
    }
    [data-testid="stMainBlockContainer"] > div:first-child [data-testid="stButton"] button:hover {
        transform: translateY(-2px);
    }
    [data-testid="stMainBlockContainer"] > div:first-child [data-testid="stButton"] button p {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.2rem;
        font-size: 0.85rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # We use columns to put refresh on left, and dark/light on right
    c1, c2, c3, c4 = st.columns([8, 1, 1, 1])
    with c1:
        if show_refresh:
            if st.button("🔄\nRefresh Page", key="top_refresh"):
                st.cache_data.clear()
                st.rerun()
    
    with c3:
        if st.button("🌙\nDark Mode", key="top_dark"):
            set_theme("dark")
            st.rerun()
        
    with c4:
        if st.button("☀️\nLight Mode", key="top_light"):
            set_theme("light")
            st.rerun()
