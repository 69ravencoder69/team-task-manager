import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from components.topbar import render_topbar
from services import api_service
from services.api_service import APIError
from utils.session_manager import init_session, is_logged_in, set_auth
from utils.theme import apply_theme

st.set_page_config(
    page_title="Register | Team Task Manager",
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
    'Create your account</p>',
    unsafe_allow_html=True,
)

# ── Register form ──────────────────────────────────────────────────────────────
with st.form("register_form"):
    st.markdown("**Name**")
    full_name = st.text_input("name", label_visibility="collapsed", placeholder="Full name")

    st.markdown("<div style='margin-top:0.5rem;'><b>Enter Email</b></div>", unsafe_allow_html=True)
    email = st.text_input("email", label_visibility="collapsed", placeholder="you@example.com")

    st.markdown("<div style='margin-top:0.5rem;'><b>Enter Password</b></div>", unsafe_allow_html=True)
    password = st.text_input("pw", type="password", label_visibility="collapsed", placeholder="Min. 6 characters")

    st.markdown("<div style='margin-top:0.5rem;'><b>Confirm Password</b></div>", unsafe_allow_html=True)
    confirm = st.text_input("cpw", type="password", label_visibility="collapsed", placeholder="Re-enter password")

    st.markdown("<div style='margin-top:0.5rem;'><b>Role</b></div>", unsafe_allow_html=True)
    role = st.selectbox("role", ["member", "admin"], label_visibility="collapsed")

    st.markdown(
        '<p style="text-align:center; font-size:0.85rem; margin:1rem 0 0.5rem;">'
        'Already a Member? <a href="login" target="_self" style="color:inherit; text-decoration:underline;">Login</a></p>',
        unsafe_allow_html=True,
    )
    submitted = st.form_submit_button("Register", use_container_width=True)

# ── Auth logic ─────────────────────────────────────────────────────────────────
if submitted:
    if not all([full_name, email, password, confirm]):
        st.error("Please fill in all fields.")
    elif password != confirm:
        st.error("Passwords do not match.")
    elif len(password) < 6:
        st.error("Password must be at least 6 characters.")
    else:
        try:
            api_service.register(email, password, full_name, role)
            result = api_service.login(email, password)
            set_auth(result["access_token"], result["user"])
            st.switch_page("pages/dashboard.py")
        except APIError as e:
            st.error(e.message)
