import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from components.topbar import render_topbar
from services import api_service
from services.api_service import APIError
from utils.session_manager import init_session, is_logged_in, set_auth
from utils.theme import apply_theme, set_theme

st.set_page_config(
    page_title="Login | Team Task Manager",
    page_icon="⚡",
    layout="centered",
)
init_session()
apply_theme()

if is_logged_in():
    st.switch_page("pages/dashboard.py")

render_topbar(show_refresh=False)

# ── Vertical breathing room ────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<h1 style="text-align:center; font-weight:800; font-size:2rem; '
    'margin-bottom:0.25rem; text-transform:uppercase; letter-spacing:0.04em;">'
    'TEAM TASK MANAGER</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p style="text-align:center; font-size:1rem; margin-bottom:1.75rem; color:#888;">'
    'Login to your account</p>',
    unsafe_allow_html=True,
)

# ── Login form (centered layout handles horizontal centering) ──────────────────
with st.form("login_form"):
    st.markdown("**Enter Email**")
    email = st.text_input("email", label_visibility="collapsed", placeholder="you@example.com")
    st.markdown("<div style='margin-top:0.5rem;'><b>Enter Password</b></div>", unsafe_allow_html=True)
    password = st.text_input("password", type="password", label_visibility="collapsed", placeholder="••••••••")

    st.markdown(
        '<p style="text-align:center; font-size:0.85rem; margin:1rem 0 0.5rem;">'
        'New User? <a href="register" target="_self" style="color:inherit; text-decoration:underline;">Register</a>'
        ' &nbsp;|&nbsp; '
        '<a href="#" style="color:inherit; text-decoration:underline;">Login as Admin</a></p>',
        unsafe_allow_html=True,
    )
    submitted = st.form_submit_button("Login", use_container_width=True)

st.markdown(
    '<p style="text-align:center; font-size:0.78rem; color:#666; margin-top:1rem;">'
    'Demo: admin@demo.com &nbsp;/&nbsp; Admin123!</p>',
    unsafe_allow_html=True,
)

# ── Auth logic ─────────────────────────────────────────────────────────────────
if submitted:
    if not email or not password:
        st.error("Please enter email and password.")
    else:
        try:
            result = api_service.login(email, password)
            set_auth(result["access_token"], result["user"])
            st.switch_page("pages/dashboard.py")
        except APIError as e:
            st.error(e.message)
