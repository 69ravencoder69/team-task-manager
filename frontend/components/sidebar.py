import streamlit as st

from utils.session_manager import get_user_email, get_user_name, is_admin, logout
from utils.theme import get_theme, set_theme

NAV_ITEMS = [
    ("Projects", "PROJECT", "📁"),
    ("Tasks", "TASK", "☰"),
    ("Dashboard", "DASHBOARD", "◷"),
    ("Analytics", "ANALYTICS", "▥"),
]


def render_sidebar(current_page: str = "Dashboard") -> str:
    with st.sidebar:
        st.markdown('<div class="ttm-brand">TEAM<br>TASK MANAGER</div>', unsafe_allow_html=True)

        selected = current_page
        for page_key, label, icon in NAV_ITEMS:
            btn_type = "primary" if page_key == current_page else "secondary"
            if st.button(f"{icon}  {label}", key=f"nav_{page_key}", use_container_width=True, type=btn_type):
                selected = page_key

        st.markdown('<p class="ttm-nav-label">Navigation</p>', unsafe_allow_html=True)
        role = "Admin" if is_admin() else "Project Manager"
        st.markdown(
            f'<div class="ttm-user-block">'
            f'<div><span>Name:</span> {get_user_name()}</div>'
            f'<div><span>Email ID:</span> {get_user_email()}</div>'
            f'<div><span>Designation:</span> {role}</div></div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")
        if st.button("⎋  LOGOUT", use_container_width=True):
            logout()
            st.switch_page("pages/login.py")

        c1, c2 = st.columns(2)
        if c1.button("🌙 Dark", use_container_width=True, type="primary" if get_theme() == "dark" else "secondary"):
            set_theme("dark")
            st.rerun()
        if c2.button("☀️ Light", use_container_width=True, type="primary" if get_theme() == "light" else "secondary"):
            set_theme("light")
            st.rerun()

    return selected
