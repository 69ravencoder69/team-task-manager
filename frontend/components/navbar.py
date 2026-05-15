from datetime import datetime

import streamlit as st

from utils.theme import THEMES, get_theme


def render_navbar(title: str, subtitle: str = "", show_refresh: bool = True):
    t = THEMES[get_theme()]
    col1, col2, col3 = st.columns([4, 1, 1])

    with col1:
        st.markdown(f"## {title}")
        if subtitle:
            st.caption(subtitle)

    with col2:
        st.markdown(
            f'<p style="text-align:right;color:{t["muted"]};font-size:0.8rem;margin-top:1.5rem;">'
            f'Updated {datetime.now().strftime("%H:%M:%S")}</p>',
            unsafe_allow_html=True,
        )

    with col3:
        if show_refresh:
            if st.button("🔄 Refresh", use_container_width=True, help="Refresh current page"):
                st.cache_data.clear()
                st.rerun()

    st.markdown(
        f'<hr style="border:none;border-top:1px solid {t["sidebar_border"]};margin:0.5rem 0 1.5rem 0;">',
        unsafe_allow_html=True,
    )
