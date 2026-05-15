import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from services import api_service
from services.api_service import APIError
from utils.session_manager import init_session, is_logged_in, set_auth
from utils.theme import apply_theme, set_theme

st.set_page_config(page_title="Register | Team Task Manager", page_icon="⚡", layout="centered")
init_session()
apply_theme()

if is_logged_in():
    st.switch_page("pages/dashboard.py")

col1, col2, col3 = st.columns([2, 1, 1])
with col2:
    if st.button("🌙", help="Dark mode"):
        set_theme("dark")
        st.rerun()
with col3:
    if st.button("☀️", help="Light mode"):
        set_theme("light")
        st.rerun()

st.markdown('<motion-div class="login-card">', unsafe_allow_html=True)
st.markdown("## Create Account")
st.caption("Join your team on Team Task Manager")

with st.form("register_form"):
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")
    submitted = st.form_submit_button("Register", use_container_width=True, type="primary")

if submitted:
    if not all([full_name, email, password, confirm]):
        st.error("All fields are required.")
    elif password != confirm:
        st.error("Passwords do not match.")
    elif len(password) < 6:
        st.error("Password must be at least 6 characters.")
    else:
        try:
            api_service.register(email, password, full_name)
            result = api_service.login(email, password)
            set_auth(result["access_token"], result["user"])
            st.success("Account created! Redirecting...")
            st.switch_page("pages/dashboard.py")
        except APIError as e:
            st.error(e.message)

if st.button("← Back to Login"):
    st.switch_page("pages/login.py")
