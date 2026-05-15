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
    st.switch_page("pages/dashboard.py")

render_topbar(show_refresh=False)

    st.markdown('<div class="ttm-auth-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="ttm-auth-card">', unsafe_allow_html=True)
    st.markdown('<p class="ttm-auth-title">Enter Your Details</p>', unsafe_allow_html=True)

    with st.form("register_form"):
        st.markdown("**Name**")
        full_name = st.text_input("name", label_visibility="collapsed")
        st.markdown("**Enter Email**")
        email = st.text_input("email", label_visibility="collapsed")
        st.markdown("**Enter Password**")
        password = st.text_input("pw", type="password", label_visibility="collapsed")
        st.markdown("**Confirm Password**")
        confirm = st.text_input("cpw", type="password", label_visibility="collapsed")
        
        st.markdown(
            '<p style="text-align:center; font-size: 0.9rem; margin: 1rem 0;">Already a Member? <a href="login" target="_self" style="color: inherit; text-decoration: underline;">Login</a></p>',
            unsafe_allow_html=True,
        )
        submitted = st.form_submit_button("Register", use_container_width=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

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
            st.switch_page("pages/dashboard.py")
        except APIError as e:
            st.error(e.message)
