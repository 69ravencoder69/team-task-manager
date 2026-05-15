import streamlit as st

from utils.theme import get_theme, set_theme


def render_topbar(show_refresh: bool = True):
    st.markdown("""
    <style>
    /* target topbar columns */
    div[data-testid="column"] button p {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.2rem;
        font-size: 0.85rem !important;
    }
    .topbar-btn-wrapper button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: var(--text-color) !important;
        padding: 0 !important;
    }
    .topbar-btn-wrapper button:hover {
        background: transparent !important;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # We use columns to put refresh on left, and dark/light on right
    c1, c2, c3, c4 = st.columns([8, 1, 1, 1])
    with c1:
        if show_refresh:
            st.markdown('<div class="topbar-btn-wrapper">', unsafe_allow_html=True)
            if st.button("🔄\nRefresh Page", key="top_refresh"):
                st.cache_data.clear()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    with c3:
        st.markdown('<div class="topbar-btn-wrapper">', unsafe_allow_html=True)
        if st.button("🌙\nDark Mode", key="top_dark"):
            set_theme("dark")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c4:
        st.markdown('<div class="topbar-btn-wrapper">', unsafe_allow_html=True)
        if st.button("☀️\nLight Mode", key="top_light"):
            set_theme("light")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
