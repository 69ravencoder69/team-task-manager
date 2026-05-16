import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from components.topbar import render_topbar
from services import api_service
from services.api_service import APIError
from utils.session_manager import init_session, is_logged_in, set_auth
from utils.theme import apply_theme, set_theme

st.set_page_config(page_title="Login | Team Task Manager", page_icon="⚡", layout="centered")
init_session()
apply_theme()

if is_logged_in():
    # Honour any pending redirect (e.g. from nav bar)
    redirect_to = st.session_state.pop("post_login_redirect", "pages/dashboard.py")
    st.switch_page(redirect_to)

render_topbar(show_refresh=False)

st.markdown('<h1 style="text-align:center; font-weight:800; font-size:2rem; margin-bottom:0.5rem; text-transform:uppercase;">TEAM TASK MANAGER</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:1.2rem; margin-bottom:1rem; color:var(--text-color);">Login Page</p>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1.2, 1])
with c2:
    with st.form("login_form"):
        st.markdown("**Enter Email**")
        email = st.text_input("email", label_visibility="collapsed")
        st.markdown("**Enter Password**")
        password = st.text_input("password", type="password", label_visibility="collapsed")

        st.markdown(
            '<p style="text-align:center; font-size: 0.9rem; margin: 1rem 0;">New User? <a href="register" target="_self" style="color: inherit; text-decoration: underline;">Register</a> | <a href="#" style="color: inherit; text-decoration: underline;">Login as Admin</a></p>',
            unsafe_allow_html=True,
        )
        submitted = st.form_submit_button("Login", use_container_width=True)

if submitted:
    if not email or not password:
        st.error("Please enter email and password.")
    else:
        try:
            result = api_service.login(email, password)
            set_auth(result["access_token"], result["user"])
            # Redirect to the page that was originally requested, or dashboard
            redirect_to = st.session_state.pop("post_login_redirect", "pages/dashboard.py")
            st.switch_page(redirect_to)
        except APIError as e:
            st.error(e.message)

st.caption("Demo: admin@demo.com / Admin123!")
