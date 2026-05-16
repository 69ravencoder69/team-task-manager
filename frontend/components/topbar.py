import streamlit as st

from utils.theme import get_theme, set_theme


def render_topbar(show_refresh: bool = True):
    """Render a full-width navigation bar using HTML/CSS + a minimal Streamlit button row for theme toggles."""

    # ── Hide Streamlit sidebar & collapse button ───────────────────────────────
    st.markdown("""
    <style>
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stSidebar"]        { display: none !important; }

    /* ── Full-width HTML navbar ─────────────────────────────────────────────── */
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
    .ttm-nav-links a:hover {
        color: #fff;
        background: rgba(255,255,255,0.08);
    }

    /* ── Theme toggle buttons (Streamlit) ───────────────────────────────────── */
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
    /* Remove any extra top padding from the block container */
    [data-testid="stMainBlockContainer"] { padding-top: 0.5rem !important; }
    </style>
    """, unsafe_allow_html=True)

    # ── HTML nav bar (brand + links) ────────────────────────────────────────────
    st.markdown("""
    <div class="ttm-navbar">
        <div class="ttm-brand">TEAM TASK MANAGER</div>
        <nav class="ttm-nav-links">
            <a href="/" target="_self">Home</a>
            <a href="/?nav=features" target="_self">Features</a>
            <a href="/login" target="_self" onclick="sessionStorage.setItem('redirect','dashboard')">Dashboard</a>
            <a href="/login" target="_self" onclick="sessionStorage.setItem('redirect','projects')">Projects</a>
            <a href="/login" target="_self" onclick="sessionStorage.setItem('redirect','analytics')">Analytics</a>
        </nav>
    </div>
    """, unsafe_allow_html=True)

    # ── Theme toggle buttons (need Streamlit for state management) ──────────────
    st.markdown('<div class="ttm-theme-row">', unsafe_allow_html=True)
    _, c_dark, c_light = st.columns([10, 1, 1])
    with c_dark:
        if st.button("🌙 Dark", key="top_dark", use_container_width=True):
            set_theme("dark")
            st.rerun()
    with c_light:
        if st.button("☀️ Light", key="top_light", use_container_width=True):
            set_theme("light")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
