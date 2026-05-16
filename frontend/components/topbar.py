import streamlit as st

from utils.theme import get_theme, set_theme


def render_topbar(show_refresh: bool = True):
    st.markdown("""
    <style>
    /* ── Theme toggle & nav buttons inside topbar ──────────────────────────── */
    [data-testid="stMainBlockContainer"] > div:first-child [data-testid="stButton"] button {
        background: transparent !important;
        border: 1px solid var(--border-color, #333) !important;
        box-shadow: none !important;
        color: var(--text-color) !important;
        padding: 0.25rem 0.75rem !important;
        min-height: 0 !important;
        font-size: 0.8rem !important;
        border-radius: 6px !important;
        transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease !important;
    }
    [data-testid="stMainBlockContainer"] > div:first-child [data-testid="stButton"] button:hover {
        background: var(--card-hover-bg, #222) !important;
        color: #fff !important;
    }
    [data-testid="stMainBlockContainer"] > div:first-child [data-testid="stButton"] button p {
        font-size: 0.8rem !important;
        margin: 0 !important;
    }
    /* Right-align columns */
    [data-testid="stMainBlockContainer"] > div:first-child [data-testid="column"] {
        display: flex;
        justify-content: flex-end;
    }

    /* ── Shared nav-link style (used on login / register) ──────────────────── */
    .topbar-nav-link button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #888 !important;
        font-size: 0.85rem !important;
        padding: 0.3rem 0.6rem !important;
        min-height: 0 !important;
        border-radius: 6px !important;
        transition: color 0.2s ease, background 0.2s ease !important;
    }
    .topbar-nav-link button:hover {
        color: #fff !important;
        background: rgba(255,255,255,0.07) !important;
    }
    .topbar-nav-link button p { margin: 0 !important; font-size: 0.85rem !important; }
    </style>
    """, unsafe_allow_html=True)

    # ── Row: brand | nav links | theme toggles ─────────────────────────────────
    c_brand, cn1, cn2, cn3, cn4, cn5, c_dark, c_light = st.columns(
        [2.5, 0.9, 0.9, 1.1, 0.9, 1.1, 1.2, 1.2]
    )

    with c_brand:
        st.markdown(
            '<div style="font-weight:800; font-size:1.1rem; letter-spacing:0.02em; '
            'padding-top:0.4rem; text-transform:uppercase;">TEAM TASK MANAGER</div>',
            unsafe_allow_html=True,
        )

    with cn1:
        st.markdown('<div class="topbar-nav-link">', unsafe_allow_html=True)
        if st.button("Home", key="tb_home", use_container_width=True):
            st.switch_page("app.py")
        st.markdown('</div>', unsafe_allow_html=True)

    with cn2:
        st.markdown('<div class="topbar-nav-link">', unsafe_allow_html=True)
        if st.button("Features", key="tb_features", use_container_width=True):
            # Go to landing page and scroll to features
            st.session_state["scroll_to_features"] = True
            st.switch_page("app.py")
        st.markdown('</div>', unsafe_allow_html=True)

    with cn3:
        st.markdown('<div class="topbar-nav-link">', unsafe_allow_html=True)
        if st.button("Dashboard", key="tb_dashboard", use_container_width=True):
            st.session_state["post_login_redirect"] = "pages/dashboard.py"
            st.switch_page("pages/login.py")
        st.markdown('</div>', unsafe_allow_html=True)

    with cn4:
        st.markdown('<div class="topbar-nav-link">', unsafe_allow_html=True)
        if st.button("Projects", key="tb_projects", use_container_width=True):
            st.session_state["post_login_redirect"] = "pages/projects.py"
            st.switch_page("pages/login.py")
        st.markdown('</div>', unsafe_allow_html=True)

    with cn5:
        st.markdown('<div class="topbar-nav-link">', unsafe_allow_html=True)
        if st.button("Analytics", key="tb_analytics", use_container_width=True):
            st.session_state["post_login_redirect"] = "pages/analytics.py"
            st.switch_page("pages/login.py")
        st.markdown('</div>', unsafe_allow_html=True)

    with c_dark:
        if st.button("🌙 Dark", key="top_dark", use_container_width=True):
            set_theme("dark")
            st.rerun()

    with c_light:
        if st.button("☀️ Light", key="top_light", use_container_width=True):
            set_theme("light")
            st.rerun()
