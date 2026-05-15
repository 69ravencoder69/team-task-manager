import streamlit as st
from streamlit_option_menu import option_menu

from utils.session_manager import get_user_name, is_admin, logout
from utils.theme import get_theme, set_theme, THEMES


def _nav_styles():
    t = THEMES[get_theme()]
    return {
        "container": {"padding": "0!important", "background-color": "transparent"},
        "icon": {"color": t["muted"], "font-size": "16px"},
        "nav-link": {
            "font-size": "14px",
            "text-align": "left",
            "margin": "4px 0",
            "padding": "10px 14px",
            "border-radius": "8px",
            "transition": "all 0.25s ease",
            "--hover-color": t["nav_hover"],
        },
        "nav-link-selected": {
            "background-color": t["nav_selected"],
            "color": "white",
            "font-weight": "600",
            "box-shadow": f"0 4px 12px {t['shadow_hover']}",
        },
    }


def render_sidebar(current_page: str = "Dashboard") -> str:
    with st.sidebar:
        st.markdown(
            f"""
            <motion-div class="nav-pane-header">
                <h3>⚡ Team Task Manager</h3>
                <span>Navigation</span>
            </motion-div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(f"### 👤 {get_user_name()}")
        role_label = "Admin" if is_admin() else "Member"
        st.caption(f"Role: **{role_label}**")

        st.divider()

        page_index = ["Dashboard", "Projects", "Tasks", "Analytics"].index(current_page)

        selected = option_menu(
            menu_title=None,
            options=["Dashboard", "Projects", "Tasks", "Analytics"],
            icons=["speedometer2", "folder", "check2-square", "bar-chart"],
            menu_icon=None,
            default_index=page_index,
            orientation="vertical",
            styles=_nav_styles(),
        )

        st.divider()

        st.markdown("**Appearance**")
        theme_col1, theme_col2 = st.columns(2)
        with theme_col1:
            if st.button("🌙 Dark", use_container_width=True, type="primary" if get_theme() == "dark" else "secondary"):
                set_theme("dark")
                st.rerun()
        with theme_col2:
            if st.button("☀️ Light", use_container_width=True, type="primary" if get_theme() == "light" else "secondary"):
                set_theme("light")
                st.rerun()

        st.divider()

        if st.button("🔄 Refresh Data", use_container_width=True, type="primary", help="Reload page data from server"):
            st.cache_data.clear()
            st.rerun()

        st.divider()

        if st.button("Logout", use_container_width=True, type="secondary"):
            logout()
            st.rerun()

    return selected
