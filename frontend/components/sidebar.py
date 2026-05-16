import streamlit as st

from utils.session_manager import get_user_email, get_user_name, is_admin, logout
from utils.theme import get_theme, set_theme

NAV_ITEMS = [
    ("Projects",   "pages/projects.py",   "📁"),
    ("Tasks",      "pages/tasks.py",      "☰"),
    ("Dashboard",  "pages/dashboard.py",  "◷"),
    ("Analytics",  "pages/analytics.py",  "▥"),
]

PAGE_KEY = {
    "pages/projects.py":   "Projects",
    "pages/tasks.py":      "Tasks",
    "pages/dashboard.py":  "Dashboard",
    "pages/analytics.py":  "Analytics",
}


def render_sidebar(current_page: str = "Dashboard") -> str:
    # ── Top nav bar (same style as topbar.py) ──────────────────────────────────
    st.markdown("""
    <style>
    /* ── Top navbar ─────────────────────────────────────────────────────────── */
    .ttm-navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.6rem 1.5rem;
        border-bottom: 1px solid #2a2a2a;
        background: transparent;
        gap: 1rem;
    }
    .ttm-brand {
        font-weight: 800;
        font-size: 1.05rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        white-space: nowrap;
        color: inherit;
    }
    .ttm-nav-links {
        display: flex;
        gap: 0.25rem;
        align-items: center;
        flex: 1;
        justify-content: center;
    }
    .ttm-nav-links a {
        color: #888;
        text-decoration: none;
        font-size: 0.85rem;
        padding: 0.3rem 0.75rem;
        border-radius: 6px;
        transition: color 0.2s ease, background 0.2s ease;
        white-space: nowrap;
    }
    .ttm-nav-links a:hover  { color: #fff; background: rgba(255,255,255,0.08); }
    .ttm-nav-links a.active { color: #fff; background: rgba(255,255,255,0.12); font-weight: 600; }

    /* ── Theme toggle buttons ───────────────────────────────────────────────── */
    .ttm-theme-row [data-testid="stButton"] button {
        background: transparent !important;
        border: 1px solid #444 !important;
        box-shadow: none !important;
        color: #aaa !important;
        padding: 0.2rem 0.65rem !important;
        min-height: 0 !important;
        font-size: 0.78rem !important;
        border-radius: 6px !important;
        white-space: nowrap !important;
        transition: background 0.2s ease, color 0.2s ease !important;
    }
    .ttm-theme-row [data-testid="stButton"] button:hover {
        background: #222 !important;
        color: #fff !important;
    }
    .ttm-theme-row [data-testid="stButton"] button p {
        margin: 0 !important;
        font-size: 0.78rem !important;
    }
    [data-testid="stMainBlockContainer"] { padding-top: 0.5rem !important; }
    </style>
    """, unsafe_allow_html=True)

    # Determine active class per link
    def active(page_key):
        return ' class="active"' if current_page == page_key else ""

    st.markdown(f"""
    <div class="ttm-navbar">
        <div class="ttm-brand">TEAM TASK MANAGER</div>
        <nav class="ttm-nav-links">
            <a href="/" target="_self">Home</a>
            <a href="/dashboard"{active("Dashboard")}>Dashboard</a>
            <a href="/projects"{active("Projects")}>Projects</a>
            <a href="/analytics"{active("Analytics")}>Analytics</a>
        </nav>
    </div>
    """, unsafe_allow_html=True)

    # Theme toggles aligned to the right
    st.markdown('<div class="ttm-theme-row">', unsafe_allow_html=True)
    _, c_dark, c_light = st.columns([10, 1, 1])
    with c_dark:
        if st.button("🌙 Dark", key="sb_top_dark", use_container_width=True):
            set_theme("dark")
            st.rerun()
    with c_light:
        if st.button("☀️ Light", key="sb_top_light", use_container_width=True):
            set_theme("light")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Left sidebar ───────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown('<div class="ttm-brand">TEAM<br>TASK MANAGER</div>', unsafe_allow_html=True)

        selected = current_page
        for page_key, route, icon in NAV_ITEMS:
            if page_key == "Analytics" and not is_admin():
                continue
            btn_type = "primary" if page_key == current_page else "secondary"
            if st.button(f"{icon}  {page_key}", key=f"nav_{page_key}", use_container_width=True, type=btn_type):
                st.switch_page(route)

        st.markdown('<p style="font-size:0.75rem; color:#888; margin:0.5rem 0 0.25rem;">Navigation</p>', unsafe_allow_html=True)
        role = "Admin" if is_admin() else "Member"
        st.markdown(
            f'<div style="font-size:0.8rem; line-height:1.8;">'
            f'<div><span style="color:#888;">Name:</span> {get_user_name()}</div>'
            f'<div><span style="color:#888;">Email:</span> {get_user_email()}</div>'
            f'<div><span style="color:#888;">Role:</span> {role}</div></div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")
        if st.button("⎋  LOGOUT", use_container_width=True):
            logout()
            st.switch_page("pages/login.py")

        c1, c2 = st.columns(2)
        if c1.button("🌙 Dark", use_container_width=True,
                     type="primary" if get_theme() == "dark" else "secondary"):
            set_theme("dark")
            st.rerun()
        if c2.button("☀️ Light", use_container_width=True,
                     type="primary" if get_theme() == "light" else "secondary"):
            set_theme("light")
            st.rerun()

    return selected
