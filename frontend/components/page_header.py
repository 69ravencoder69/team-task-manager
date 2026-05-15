import streamlit as st

from components.topbar import render_topbar


def render_page_header(title: str, subtitle: str = ""):
    render_topbar()
    st.markdown(f'<p class="ttm-page-title">{title}</p>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<p class="ttm-page-sub">{subtitle}</p>', unsafe_allow_html=True)
    st.markdown('<hr class="ttm-divider">', unsafe_allow_html=True)
