import streamlit as st

THEMES = {
    "dark": {
        "bg": "#0a0a0a",
        "sidebar": "#111111",
        "sidebar_border": "#2a2a2a",
        "card": "#1a1a1a",
        "card_hover": "#222222",
        "input_bg": "#1a1a1a",
        "text": "#e5e5e5",
        "heading": "#ffffff",
        "muted": "#9ca3af",
        "border": "#333333",
        "btn_bg": "#2a2a2a",
        "btn_text": "#ffffff",
        "btn_primary_bg": "#f5f5f5",
        "btn_primary_text": "#0a0a0a",
        "nav_active": "#2d2d2d",
        "badge_todo_bg": "#1e3a5f",
        "badge_todo_text": "#93c5fd",
        "badge_progress_bg": "#422006",
        "badge_progress_text": "#fcd34d",
        "badge_done_bg": "#14532d",
        "badge_done_text": "#86efac",
    },
    "light": {
        "bg": "#d4d4d4",
        "sidebar": "#c8c8c8",
        "sidebar_border": "#1a1a1a",
        "card": "#e8e8e8",
        "card_hover": "#f0f0f0",
        "input_bg": "#ffffff",
        "text": "#1a1a1a",
        "heading": "#000000",
        "muted": "#4b5563",
        "border": "#1a1a1a",
        "btn_bg": "#d1d1d1",
        "btn_text": "#000000",
        "btn_primary_bg": "#ffffff",
        "btn_primary_text": "#000000",
        "nav_active": "#b8b8b8",
        "badge_todo_bg": "#dbeafe",
        "badge_todo_text": "#1e40af",
        "badge_progress_bg": "#fef3c7",
        "badge_progress_text": "#92400e",
        "badge_done_bg": "#dcfce7",
        "badge_done_text": "#166534",
    },
}


def get_theme() -> str:
    return st.session_state.get("theme", "dark")


def set_theme(theme: str):
    st.session_state.theme = theme if theme in THEMES else "dark"


def get_colors():
    return THEMES[get_theme()]


def apply_theme():
    t = THEMES[get_theme()]
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif !important;
        }}

        .stApp {{
            background: {t["bg"]} !important;
            color: {t["text"]} !important;
        }}

        #MainMenu, footer, header {{visibility: hidden;}}

        [data-testid="stSidebar"] {{
            background: {t["sidebar"]} !important;
            border-right: 1px solid {t["border"]} !important;
        }}
        [data-testid="stSidebar"] > div:first-child {{
            padding-top: 1.5rem;
        }}

        [data-testid="stMetricValue"] {{
            color: {t["heading"]} !important;
            font-size: 2.25rem !important;
            font-weight: 700 !important;
        }}
        [data-testid="stMetricLabel"] {{
            color: {t["muted"]} !important;
            font-size: 0.8rem !important;
            text-transform: capitalize;
        }}
        [data-testid="stMetric"] {{
            background: {t["card"]};
            border: 1px solid {t["border"]};
            border-radius: 10px;
            padding: 1rem 1.25rem;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        [data-testid="stMetric"]:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.25);
        }}

        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div,
        .stDateInput > div > div > input {{
            background: {t["input_bg"]} !important;
            color: {t["heading"]} !important;
            border: 1px solid {t["border"]} !important;
            border-radius: 8px !important;
        }}

        .stButton > button {{
            border: 1px solid {t["border"]} !important;
            border-radius: 10px !important;
            background: {t["btn_bg"]} !important;
            color: {t["btn_text"]} !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }}
        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}
        .stButton > button[kind="primary"] {{
            background: {t["btn_primary_bg"]} !important;
            color: {t["btn_primary_text"]} !important;
            border: 1px solid {t["border"]} !important;
        }}

        h1, h2, h3, h4 {{ color: {t["heading"]} !important; }}

        /* Brand sidebar */
        .ttm-brand {{
            font-size: 1.35rem;
            font-weight: 800;
            letter-spacing: 0.04em;
            line-height: 1.2;
            color: {t["heading"]};
            margin-bottom: 2rem;
            text-transform: uppercase;
        }}
        .ttm-nav-label {{
            font-size: 0.65rem;
            letter-spacing: 0.15em;
            color: {t["muted"]};
            margin: 1.5rem 0 0.75rem 0;
            text-transform: uppercase;
        }}
        .ttm-user-block {{
            font-size: 0.85rem;
            color: {t["text"]};
            line-height: 1.8;
            margin-top: 1rem;
        }}
        .ttm-user-block span {{
            color: {t["muted"]};
        }}

        /* Page header */
        .ttm-page-title {{
            font-size: 2.75rem;
            font-weight: 800;
            letter-spacing: 0.02em;
            color: {t["heading"]};
            margin: 0;
            text-transform: uppercase;
        }}
        .ttm-page-sub {{
            color: {t["muted"]};
            font-size: 1rem;
            margin: 0.25rem 0 1rem 0;
        }}
        .ttm-divider {{
            border: none;
            border-top: 1px solid {t["border"]};
            margin: 1rem 0 1.5rem 0;
        }}

        /* Auth card */
        .ttm-auth-wrap {{
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 70vh;
        }}
        .ttm-auth-card {{
            background: {t["card"]};
            border: 1px solid {t["border"]};
            border-radius: 12px;
            padding: 2.5rem 2.75rem;
            width: 100%;
            max-width: 420px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.15);
        }}
        .ttm-auth-title {{
            text-align: center;
            font-size: 1.75rem;
            font-weight: 700;
            color: {t["heading"]};
            margin-bottom: 1.5rem;
        }}

        /* Stat / project / task cards */
        .ttm-card {{
            background: {t["card"]};
            border: 1px solid {t["border"]};
            border-radius: 10px;
            padding: 1rem 1.25rem;
            margin-bottom: 0.75rem;
            transition: all 0.2s ease;
        }}
        .ttm-card:hover {{
            background: {t["card_hover"]};
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.2);
        }}

        .ttm-project-row {{
            display: grid;
            grid-template-columns: auto 2fr 1fr 1fr 1fr auto;
            gap: 1rem;
            align-items: center;
            background: {t["card"]};
            border: 1px solid {t["border"]};
            border-radius: 10px;
            padding: 1.25rem;
            margin-bottom: 0.5rem;
            transition: all 0.2s ease;
        }}
        .ttm-project-row:hover {{
            background: {t["card_hover"]};
            border-color: {t["muted"]};
        }}

        .ttm-task-row {{
            display: grid;
            grid-template-columns: 2fr 2fr 1fr;
            gap: 1rem;
            align-items: center;
            padding: 1rem 0;
            border-bottom: 1px solid {t["border"]};
        }}
        .ttm-task-row:hover {{
            background: {t["card_hover"]};
        }}

        .ttm-badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .ttm-badge-todo {{ background: {t["badge_todo_bg"]}; color: {t["badge_todo_text"]}; }}
        .ttm-badge-progress {{ background: {t["badge_progress_bg"]}; color: {t["badge_progress_text"]}; }}
        .ttm-badge-done {{ background: {t["badge_done_bg"]}; color: {t["badge_done_text"]}; }}

        .ttm-stat-label {{
            font-size: 0.8rem;
            color: {t["muted"]};
            margin-bottom: 0.25rem;
        }}
        .ttm-stat-value {{
            font-size: 2rem;
            font-weight: 700;
            color: {t["heading"]};
        }}

        /* Top bar */
        .ttm-topbar {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 0.5rem;
        }}

        /* Search pill */
        .ttm-search-hint {{
            color: {t["muted"]};
            font-size: 0.85rem;
            margin-bottom: 0.35rem;
        }}

        /* Hide streamlit option menu default padding */
        .streamlit-expanderHeader {{
            font-weight: 600 !important;
            color: {t["heading"]} !important;
        }}

        div[data-testid="stExpander"] {{
            background: {t["card"]};
            border: 1px solid {t["border"]};
            border-radius: 10px;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
