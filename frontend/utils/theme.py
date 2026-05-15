import streamlit as st

THEMES = {
    "dark": {
        "bg": "#121212",
        "sidebar": "#121212",
        "sidebar_border": "#1a1a1a",
        "card": "#1e1e1e",
        "card_hover": "#252525",
        "input_bg": "#1e1e1e",
        "text": "#e5e5e5",
        "heading": "#ffffff",
        "muted": "#888888",
        "border": "#333333",
        "btn_bg": "#2a2a2a",
        "btn_text": "#ffffff",
        "btn_primary_bg": "#ffffff",
        "btn_primary_text": "#000000",
        "nav_active": "#2d2d2d",
        "badge_todo_bg": "#1e3a5f",
        "badge_todo_text": "#93c5fd",
        "badge_progress_bg": "#422006",
        "badge_progress_text": "#fcd34d",
        "badge_done_bg": "#14532d",
        "badge_done_text": "#86efac",
    },
    "light": {
        "bg": "#e5e5e5",
        "sidebar": "#e5e5e5",
        "sidebar_border": "#1a1a1a",
        "card": "#d4d4d4",
        "card_hover": "#cccccc",
        "input_bg": "#ffffff",
        "text": "#111111",
        "heading": "#000000",
        "muted": "#555555",
        "border": "#111111",
        "btn_bg": "#2d2d2d",
        "btn_text": "#ffffff",
        "btn_primary_bg": "#2d2d2d",
        "btn_primary_text": "#ffffff",
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
    
    # In light mode, auth forms should have a transparent button with a border
    auth_btn_bg = "transparent" if get_theme() == "light" else t["btn_bg"]
    auth_btn_text = "#000000" if get_theme() == "light" else t["btn_text"]
    auth_btn_border = f'1px solid {t["border"]}' if get_theme() == "light" else "none"

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

        /* Hide header/footer but keep sidebar */
        #MainMenu, footer, header {{visibility: hidden;}}

        [data-testid="stSidebarNav"] {{ display: none !important; }}

        [data-testid="stSidebar"] {{
            background: {t["sidebar"]} !important;
            border-right: 1px solid {t["border"]} !important;
        }}
        
        [data-testid="stSidebar"] > div:first-child {{
            padding-top: 1.5rem;
        }}

        /* Brand sidebar */
        .ttm-brand {{
            font-size: 1.3rem;
            font-weight: 800;
            letter-spacing: 0.02em;
            line-height: 1.2;
            color: {t["heading"]};
            margin-bottom: 2rem;
            text-transform: uppercase;
        }}
        .ttm-nav-label {{
            font-size: 0.75rem;
            letter-spacing: 0.1em;
            color: {t["muted"]};
            margin: 2rem 0 0.5rem 0;
            text-transform: uppercase;
        }}
        .ttm-user-block {{
            font-size: 0.85rem;
            color: {t["text"]};
            line-height: 1.8;
            margin-top: 0.5rem;
            padding-bottom: 2rem;
        }}
        .ttm-user-block span {{
            color: {t["muted"]};
        }}
        
        /* Specific sidebar button styling */
        [data-testid="stSidebar"] .stButton > button {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            color: {t["muted"]} !important;
            justify-content: flex-start !important;
            padding: 0.75rem 1rem !important;
            font-size: 0.95rem !important;
            font-weight: 500 !important;
            border-radius: 8px !important;
        }}
        
        [data-testid="stSidebar"] .stButton > button:hover {{
            color: {t["heading"]} !important;
            background: {t["card_hover"]} !important;
        }}
        
        [data-testid="stSidebar"] .stButton > button[kind="primary"] {{
            background: {t["border"]} !important; /* Active state like DASHBOARD in image */
            color: {t["heading"]} !important;
        }}
        /* Fix top padding gap */
        [data-testid="stMainBlockContainer"] {{
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
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
            border-radius: 8px;
            padding: 1rem 1.25rem;
            box-shadow: none;
        }}

        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div,
        .stDateInput > div > div > input {{
            background: {t["input_bg"]} !important;
            color: {t["heading"]} !important;
            border: 1px solid {t["border"]} !important;
            border-radius: 4px !important;
            padding: 0.5rem !important;
        }}

        /* Standard buttons (like tasks page) */
        .stButton > button {{
            border: 1px solid {t["border"]} !important;
            border-radius: 4px !important;
            background: {t["btn_bg"]} !important;
            color: {t["btn_text"]} !important;
            font-weight: 500 !important;
            padding: 0.5rem 1rem !important;
        }}
        
        /* Form submit buttons (Login / Register) */
        .stFormSubmitButton > button {{
            background: {auth_btn_bg} !important;
            color: {auth_btn_text} !important;
            border: {auth_btn_border} !important;
            border-radius: 4px !important;
            font-weight: 500 !important;
        }}

        h1, h2, h3, h4 {{ color: {t["heading"]} !important; }}

        /* Page header */
        .ttm-page-title {{
            font-size: 3rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: {t["heading"]};
            margin: 0;
            text-transform: uppercase;
        }}
        .ttm-page-sub {{
            color: {t["muted"]};
            font-size: 1rem;
            margin: 0.25rem 0 2rem 0;
        }}
        .ttm-divider {{
            display: none; /* Removed divider based on images */
        }}

        /* Auth card */
        .ttm-auth-wrap {{
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 80vh;
        }}
        .ttm-auth-card {{
            background: {t["card"]};
            border: 1px solid {t["border"]};
            border-radius: 8px;
            padding: 2.5rem 2.5rem;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            margin: 0 auto;
        }}
        .ttm-auth-title {{
            text-align: center;
            font-size: 2rem;
            font-weight: 600;
            color: {t["heading"]};
            margin-bottom: 1.5rem;
        }}

        .ttm-card {{
            background: {t["card"]};
            border: 1px solid {t["border"]};
            border-radius: 8px;
            padding: 1rem 1.25rem;
            margin-bottom: 0.75rem;
        }}

        .ttm-project-row {{
            display: grid;
            grid-template-columns: auto 2fr 1fr 1fr 1fr auto;
            gap: 1rem;
            align-items: center;
            background: {t["card"]};
            border: 1px solid {t["border"]};
            border-radius: 8px;
            padding: 1.25rem;
            margin-bottom: 0.5rem;
        }}

        .ttm-task-row {{
            display: grid;
            grid-template-columns: 2fr 2fr 1fr;
            gap: 1rem;
            align-items: center;
            padding: 1rem 0;
            border-bottom: 1px solid {t["border"]};
        }}

        .ttm-badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 500;
        }}
        .ttm-badge-todo {{ background: {t["badge_todo_bg"]}; color: {t["badge_todo_text"]}; }}
        .ttm-badge-progress {{ background: {t["badge_progress_bg"]}; color: {t["badge_progress_text"]}; }}
        .ttm-badge-done {{ background: {t["badge_done_bg"]}; color: {t["badge_done_text"]}; }}

        /* Search pill - matched from tasks page */
        .ttm-search-hint {{
            color: {t["muted"]};
            font-size: 0.85rem;
            margin-bottom: 0.35rem;
        }}
        .stTextInput[data-testid="stTextInput"] > div > div > input {{
            border-radius: 999px !important;
            padding-left: 2rem !important;
        }}
        
        /* Insert search icon inside input via CSS pseudo-element hack is tricky in Streamlit, 
           so we just rely on standard appearance or use emojis in placeholder */
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
