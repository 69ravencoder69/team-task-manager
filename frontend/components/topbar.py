import streamlit as st

from utils.theme import get_theme, set_theme


def render_topbar(show_refresh: bool = True):
    st.markdown("""
    <style>
    /* Styling for topbar buttons */
    [data-testid="stMainBlockContainer"] > div:first-child [data-testid="stButton"] button {
        background: transparent !important;
        border: 1px solid var(--border-color, #333) !important;
        box-shadow: none !important;
        color: var(--text-color) !important;
        padding: 0.25rem 0.75rem !important;
        min-height: 0 !important;
        font-size: 0.8rem !important;
        border-radius: 6px !important;
    }
    [data-testid="stMainBlockContainer"] > div:first-child [data-testid="stButton"] button:hover {
        background: var(--card-hover-bg, #222) !important;
    }
    [data-testid="stMainBlockContainer"] > div:first-child [data-testid="stButton"] button p {
        font-size: 0.8rem !important;
        margin: 0 !important;
    }
    /* Right align the columns */
    [data-testid="stMainBlockContainer"] > div:first-child [data-testid="column"] {
        display: flex;
        justify-content: flex-end;
    }
    </style>
    """, unsafe_allow_html=True)

    # We use columns to put refresh on left, and dark/light on right
    c_spacer, c_dark, c_light = st.columns([10, 1.5, 1.5])

    with c_dark:
        if st.button("🌙 Dark", key="top_dark", use_container_width=True):
            set_theme("dark")
            st.rerun()

    with c_light:
        if st.button("☀️ Light", key="top_light", use_container_width=True):
            set_theme("light")
            st.rerun()
