import streamlit as st


def init_session():
    defaults = {"token": None, "user": None, "role": None, "theme": "dark"}
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def is_logged_in() -> bool:
    return st.session_state.get("token") is not None


def is_admin() -> bool:
    return st.session_state.get("role") == "admin"


def set_auth(token: str, user: dict):
    st.session_state.token = token
    st.session_state.user = user
    st.session_state.role = user.get("role")


def logout():
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.role = None


def require_auth():
    if not is_logged_in():
        st.warning("Please log in to access this page.")
        st.stop()


def get_user_name() -> str:
    user = st.session_state.get("user") or {}
    return user.get("full_name", "User")


def get_user_email() -> str:
    user = st.session_state.get("user") or {}
    return user.get("email", "user@email.com")
