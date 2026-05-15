import streamlit as st

from utils.session_manager import init_session
from utils.theme import apply_theme, get_theme

PAGE_ROUTES = {
    "Dashboard": "pages/dashboard.py",
    "Projects": "pages/projects.py",
    "Tasks": "pages/tasks.py",
    "Analytics": "pages/analytics.py",
}


def init_page(require_login: bool = True):
    init_session()
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"
    apply_theme()
    if require_login:
        from utils.session_manager import require_auth
        require_auth()


def navigate_if_needed(current: str, selected: str):
    if selected != current:
        st.switch_page(PAGE_ROUTES[selected])
