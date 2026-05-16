import streamlit as st

from utils.theme import get_theme, set_theme


def render_topbar(show_refresh: bool = True):
    st.markdown("""
    <style>
    /* Remove default top padding */
    [data-testid="stMainBlockContainer"] { padding-top: 0 !important; }

    /* Hide sidebar & collapse button on auth pages */
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stSidebar"]        { display: none !important; }

    /* ── Top bar row styling ─────────────────────────────────────────────────── */
    .ttm-topbar-row [data-testid="stButton"] button {
        background: transparent !important;
        border: 1px solid #3a3a3a !important;
        box-shadow: none !important;
        color: #aaa !important;
        padding: 0.25rem 0.8rem !important;
        min-height: 0 !important;
        font-size: 0.78rem !important;
        border-radius: 6px !important;
        transition: background 0.2s ease, color 0.2s ease !important;
        white-space: nowrap !important;
    }
    .ttm-topbar-row [data-testid="stButton"] button:hover {
        background: #2a2a2a !important;
        color: #fff !important;
    }
    .ttm-topbar-row [data-testid="stButton"] button p {
        font-size: 0.78rem !important;
        margin: 0 !important;
    }
    /* Push theme buttons to right edge */
    .ttm-topbar-row [data-testid="column"]:last-child,
    .ttm-topbar-row [data-testid="column"]:nth-last-child(2) {
        display: flex !important;
        justify-content: flex-end !important;
    }

    /* ── Divider under topbar ────────────────────────────────────────────────── */
    .ttm-topbar-divider {
        border: none;
        border-top: 1px solid #2a2a2a;
        margin: 0 0 2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Header row: Brand (left) | Dark | Light ───────────────────────────────
    st.markdown('<div class="ttm-topbar-row">', unsafe_allow_html=True)
    c_brand, c_dark, c_light = st.columns([5, 2, 2])

    with c_brand:
        st.markdown(
            '<div style="font-weight:800; font-size:1rem; letter-spacing:0.05em; '
            'text-transform:uppercase; padding-top:0.35rem; white-space:nowrap;">'
            'TEAM TASK MANAGER</div>',
            unsafe_allow_html=True,
        )

    with c_dark:
        if st.button("🌙 Dark", key="top_dark", use_container_width=True):
            set_theme("dark")
            st.rerun()

    with c_light:
        if st.button("☀️ Light", key="top_light", use_container_width=True):
            set_theme("light")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<hr class="ttm-topbar-divider">', unsafe_allow_html=True)
