import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from services import api_service
from services.api_service import APIError
from utils.session_manager import init_session, is_logged_in, set_auth
from utils.theme import apply_theme, set_theme

st.set_page_config(page_title="Login | Team Task Manager", page_icon="⚡", layout="centered")
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
st.markdown("## ⚡ Team Task Manager")
st.caption("Sign in to manage your team's projects and tasks")

with st.form("login_form"):
    email = st.text_input("Email", placeholder="admin@demo.com")
    password = st.text_input("Password", type="password", placeholder="Admin123!")
    submitted = st.form_submit_button("Login", use_container_width=True, type="primary")

if submitted:
    if not email or not password:
        st.error("Please enter email and password.")
    else:
        try:
            result = api_service.login(email, password)
            set_auth(result["access_token"], result["user"])
            st.success(f"Welcome, {result['user']['full_name']}!")
            st.switch_page("pages/dashboard.py")
        except APIError as e:
            st.error(e.message)

st.divider()
st.markdown("Don't have an account?")
if st.button("Create Account", use_container_width=True):
    st.switch_page("pages/register.py")

st.info("**Demo:** admin@demo.com / Admin123!  ·  alex@demo.com / Member123!")
