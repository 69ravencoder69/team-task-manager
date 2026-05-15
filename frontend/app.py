import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st

from utils.session_manager import init_session, is_logged_in
from utils.theme import apply_theme

st.set_page_config(
    page_title="Team Task Manager",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session()
apply_theme()

if not is_logged_in():
    st.switch_page("pages/login.py")
else:
    st.switch_page("pages/dashboard.py")
