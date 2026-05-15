import streamlit as st

THEMES = {
    "dark": {
        "bg": "linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%)",
        "sidebar": "#16162a",
        "sidebar_border": "#2a2a4a",
        "card": "linear-gradient(135deg, #1e1e2e 0%, #2a2a3e 100%)",
        "card_hover": "linear-gradient(135deg, #252540 0%, #353550 100%)",
        "input_bg": "#1e1e2e",
        "text": "#e0e0e0",
        "heading": "#ffffff",
        "muted": "#aaa",
        "accent": "#6C63FF",
        "nav_selected": "#6C63FF",
        "nav_hover": "rgba(108, 99, 255, 0.25)",
        "metric": "#6C63FF",
        "shadow": "rgba(0,0,0,0.35)",
        "shadow_hover": "rgba(108, 99, 255, 0.35)",
    },
    "light": {
        "bg": "linear-gradient(180deg, #f5f7fb 0%, #e8ecf4 100%)",
        "sidebar": "#ffffff",
        "sidebar_border": "#dde3ef",
        "card": "linear-gradient(135deg, #ffffff 0%, #f8f9fc 100%)",
        "card_hover": "linear-gradient(135deg, #ffffff 0%, #eef1f8 100%)",
        "input_bg": "#ffffff",
        "text": "#2d3748",
        "heading": "#1a202c",
        "muted": "#718096",
        "accent": "#6C63FF",
        "nav_selected": "#6C63FF",
        "nav_hover": "rgba(108, 99, 255, 0.12)",
        "metric": "#6C63FF",
        "shadow": "rgba(0,0,0,0.08)",
        "shadow_hover": "rgba(108, 99, 255, 0.2)",
    },
}


def get_theme() -> str:
    return st.session_state.get("theme", "dark")


def set_theme(theme: str):
    st.session_state.theme = theme if theme in THEMES else "dark"


def toggle_theme():
    set_theme("light" if get_theme() == "dark" else "dark")


def apply_theme():
    t = THEMES[get_theme()]
    css = f"""
    <style>
        .stApp {{
            background: {t["bg"]};
            color: {t["text"]};
            transition: background 0.35s ease, color 0.35s ease;
        }}
        [data-testid="stSidebar"] {{
            background: {t["sidebar"]} !important;
            border-right: 1px solid {t["sidebar_border"]};
            box-shadow: 4px 0 24px {t["shadow"]};
        }}
        [data-testid="stSidebar"] .stMarkdown h3,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label {{
            color: {t["heading"]} !important;
        }}
        [data-testid="stMetricValue"] {{
            color: {t["metric"]} !important;
            font-size: 2rem !important;
            transition: transform 0.2s ease;
        }}
        [data-testid="stMetric"]:hover [data-testid="stMetricValue"] {{
            transform: scale(1.05);
        }}
        [data-testid="stMetricLabel"] {{
            color: {t["muted"]} !important;
        }}
        .stButton > button {{
            border-radius: 8px !important;
            transition: all 0.25s ease !important;
        }}
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 16px {t["shadow_hover"]};
        }}
        .stButton > button[kind="primary"] {{
            background: linear-gradient(90deg, {t["accent"]}, #8B5CF6) !important;
            border: none !important;
            color: white !important;
        }}
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div {{
            background: {t["input_bg"]} !important;
            color: {t["heading"]} !important;
            border: 1px solid {t["sidebar_border"]} !important;
            border-radius: 8px !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }}
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {{
            border-color: {t["accent"]} !important;
            box-shadow: 0 0 0 2px {t["nav_hover"]} !important;
        }}
        h1, h2, h3, h4 {{
            color: {t["heading"]} !important;
        }}
        p, .stCaption, [data-testid="stMarkdownContainer"] p {{
            color: {t["text"]};
        }}

        /* Navigation pane */
        .nav-pane-header {{
            background: linear-gradient(135deg, {t["accent"]}22, {t["accent"]}08);
            border: 1px solid {t["sidebar_border"]};
            border-radius: 12px;
            padding: 14px 16px;
            margin-bottom: 16px;
            transition: box-shadow 0.3s ease;
        }}
        .nav-pane-header:hover {{
            box-shadow: 0 8px 24px {t["shadow_hover"]};
        }}
        .nav-pane-header h3 {{
            margin: 0;
            color: {t["heading"]} !important;
            font-size: 1.1rem;
        }}
        .nav-pane-header span {{
            color: {t["muted"]};
            font-size: 0.85rem;
        }}

        /* Hover cards */
        .hover-card {{
            background: {t["card"]};
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            border: 1px solid {t["sidebar_border"]};
            box-shadow: 0 4px 12px {t["shadow"]};
            transition: transform 0.25s ease, box-shadow 0.25s ease, background 0.25s ease;
            cursor: default;
        }}
        .hover-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 28px {t["shadow_hover"]};
            background: {t["card_hover"]};
        }}

        /* Task cards */
        .task-card-hover {{
            background: {t["card"]};
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 4px 8px {t["shadow"]};
            transition: transform 0.25s ease, box-shadow 0.25s ease, background 0.25s ease;
        }}
        .task-card-hover:hover {{
            transform: translateY(-3px) scale(1.01);
            box-shadow: 0 10px 24px {t["shadow_hover"]};
            background: {t["card_hover"]};
        }}

        /* Project cards */
        .project-card {{
            background: {t["card"]};
            border: 1px solid {t["sidebar_border"]};
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 12px;
            transition: all 0.25s ease;
        }}
        .project-card:hover {{
            transform: translateX(4px);
            border-color: {t["accent"]};
            box-shadow: 0 8px 20px {t["shadow_hover"]};
        }}

        .login-card {{
            background: {t["card"]};
            padding: 2rem;
            border-radius: 16px;
            border: 1px solid {t["sidebar_border"]};
            box-shadow: 0 8px 32px {t["shadow_hover"]};
            transition: box-shadow 0.3s ease;
        }}
        .login-card:hover {{
            box-shadow: 0 12px 40px {t["shadow_hover"]};
        }}

        /* Refresh button highlight */
        div[data-testid="column"] .stButton > button.refresh-btn {{
            border: 1px dashed {t["accent"]} !important;
        }}

        /* Expander hover */
        .streamlit-expanderHeader:hover {{
            color: {t["accent"]} !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
