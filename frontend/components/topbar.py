import streamlit as st

from utils.theme import get_theme, set_theme


def render_topbar(show_refresh: bool = True):
    """Refresh + Dark/Light toggle — matches mock top-right."""
    col1, col2, col3, col4 = st.columns([6, 1, 1, 1])
    with col2:
        if show_refresh:
            if st.button("↻ Refresh", key="top_refresh", help="Refresh page data"):
                st.cache_data.clear()
                st.rerun()
    with col3:
        if st.button("🌙 Dark", key="top_dark", type="primary" if get_theme() == "dark" else "secondary"):
            set_theme("dark")
            st.rerun()
    with col4:
        if st.button("☀️ Light", key="top_light", type="primary" if get_theme() == "light" else "secondary"):
            set_theme("light")
            st.rerun()
