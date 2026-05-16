import streamlit as st

from utils.theme import get_theme, set_theme


def render_topbar(show_refresh: bool = True):
    st.markdown("""
    <style>
    /* Remove default top padding */
    [data-testid="stMainBlockContainer"] { padding-top: 0 !important; }

    /* ── Top bar row styling ─────────────────────────────────────────────────── */
    .ttm-topbar-row {
        padding: 0.5rem 0;
        align-items: center;
    }
    
    .ttm-topbar-row [data-testid="stButton"] button {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: none !important;
        color: #aaa !important;
        padding: 0.4rem 1rem !important;
        min-height: 0 !important;
        font-size: 0.85rem !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        white-space: nowrap !important;
        width: 100%;
    }
    
    .ttm-topbar-row [data-testid="stButton"] button:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        color: #fff !important;
        transform: translateY(-1px);
    }
    
    .ttm-topbar-row [data-testid="stButton"] button p {
        font-size: 0.85rem !important;
        margin: 0 !important;
        font-weight: 500 !important;
    }

    /* Column Alignment */
    .ttm-topbar-row [data-testid="column"] {
        display: flex !important;
        align-items: center !important;
    }
    
    /* Right-aligned columns for theme buttons */
    .ttm-topbar-row [data-testid="column"]:last-child,
    .ttm-topbar-row [data-testid="column"]:nth-last-child(2) {
        justify-content: flex-end !important;
    }

    /* ── Divider under topbar ────────────────────────────────────────────────── */
    .ttm-topbar-divider {
        border: none;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        margin: 0 0 1.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Header row ─────────────────────────────────────────────────────────────
    # Layout: [Refresh?] [Brand] [spacer] [Dark] [Light]
    st.markdown('<div class="ttm-topbar-row">', unsafe_allow_html=True)

    if show_refresh:
        # Ratios adjusted to give buttons more room: [Refresh] [Brand] [Spacer] [Dark] [Light]
        cols = st.columns([1.5, 3.5, 3, 1.5, 1.5])
        with cols[0]:
            if st.button("🔄 Refresh", key="top_refresh", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
        brand_col = cols[1]
        dark_col = cols[3]
        light_col = cols[4]
    else:
        # Layout for Login/Register (no refresh)
        cols = st.columns([4, 4, 2, 2])
        brand_col = cols[0]
        dark_col = cols[2]
        light_col = cols[3]

    with brand_col:
        st.markdown(
            '<div style="font-weight:800; font-size:1rem; letter-spacing:0.06em; '
            'text-transform:uppercase; padding-top:0.1rem; color:#fff; white-space:nowrap;">'
            'TEAM TASK MANAGER</div>',
            unsafe_allow_html=True,
        )

    with dark_col:
        if st.button("🌙 Dark", key="top_dark", use_container_width=True):
            set_theme("dark")
            st.rerun()

    with light_col:
        if st.button("☀️ Light", key="top_light", use_container_width=True):
            set_theme("light")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<hr class="ttm-topbar-divider">', unsafe_allow_html=True)
