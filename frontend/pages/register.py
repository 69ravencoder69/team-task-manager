import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from components.topbar import render_topbar
from services import api_service
from services.api_service import APIError
from utils.session_manager import init_session, is_logged_in, set_auth
from utils.theme import apply_theme

st.set_page_config(page_title="Register | Team Task Manager", page_icon="⚡", layout="centered")
init_session()
apply_theme()

if is_logged_in():
    redirect_to = st.session_state.pop("post_login_redirect", "pages/dashboard.py")
    st.switch_page(redirect_to)

render_topbar(show_refresh=False)

st.markdown('<h1 style="text-align:center; font-weight:800; font-size:2rem; margin-bottom:0.5rem; text-transform:uppercase;">TEAM TASK MANAGER</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:1.2rem; margin-bottom:1rem; color:var(--text-color);">Enter Your Details</p>', unsafe_allow_html=True)

# Center the form
c1, c2, c3 = st.columns([1, 1.2, 1])
with c2:
    with st.form("register_form"):
        st.markdown("**Name**")
        full_name = st.text_input("name", label_visibility="collapsed")
        st.markdown("**Enter Email**")
        email = st.text_input("email", label_visibility="collapsed")
        st.markdown("**Enter Password**")
        password = st.text_input("pw", type="password", label_visibility="collapsed")
        st.markdown("**Confirm Password**")
        confirm = st.text_input("cpw", type="password", label_visibility="collapsed")
        st.markdown("**Role**")
        role = st.selectbox("role", ["member", "admin"], label_visibility="collapsed")

        st.markdown(
            '<p style="text-align:center; font-size: 0.9rem; margin: 1rem 0;">Already a Member? <a href="login" target="_self" style="color: inherit; text-decoration: underline;">Login</a></p>',
            unsafe_allow_html=True,
        )
        submitted = st.form_submit_button("Register", use_container_width=True)

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
            redirect_to = st.session_state.pop("post_login_redirect", "pages/dashboard.py")
            st.switch_page(redirect_to)
        except APIError as e:
            st.error(e.message)
