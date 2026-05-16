import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st

from utils.session_manager import init_session, is_logged_in
from utils.theme import apply_theme

st.set_page_config(
    page_title="Team Task Manager",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session()
apply_theme()

if is_logged_in():
    st.switch_page("pages/dashboard.py")

# Ensure sidebar is hidden for landing page
st.markdown("""
<style>
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# Top Nav
nav_c1, nav_c2, nav_c3 = st.columns([2, 5, 1])
with nav_c1:
    st.markdown('<div style="font-weight:800; font-size:1.2rem; letter-spacing:0.02em; padding-top:0.5rem; text-transform:uppercase;">TEAM TASK MANAGER</div>', unsafe_allow_html=True)
with nav_c2:
    st.markdown("""
        <div style="display:flex; gap:1.5rem; justify-content:center; padding-top:0.75rem; font-size:0.85rem; color:#888;">
            <span>Home</span>
            <span>Features</span>
            <span>Dashboard</span>
            <span>Projects</span>
            <span>Analytics</span>
        </div>
    """, unsafe_allow_html=True)
with nav_c3:
    if st.button("Login", key="top_login", use_container_width=True):
        st.switch_page("pages/login.py")

st.markdown("<br><br><br>", unsafe_allow_html=True)

# Hero Section
st.markdown('<h1 style="font-size:3.5rem; font-weight:800; line-height:1.1; margin-bottom:1rem;">Manage Your Team<br>Tasks Efficiently</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#888; font-size:1.1rem; line-height:1.6; margin-bottom:2rem;">Organize projects, track progress, manage tasks, and improve team productivity from one simple dashboard.</p>', unsafe_allow_html=True)

bc1, bc2, bc3 = st.columns([1, 1, 6])
with bc1:
    if st.button("Get Started", type="primary", use_container_width=True):
        st.switch_page("pages/register.py")
with bc2:
    if st.button("Login", use_container_width=True):
        st.switch_page("pages/login.py")

st.markdown("<br><br><br><br>", unsafe_allow_html=True)

# Features Section
st.markdown('<h2 style="text-align:center; margin-bottom:3rem;">Features</h2>', unsafe_allow_html=True)
f1, f2, f3 = st.columns(3)

def feature_card(icon, title, desc):
    return f"""
    <div style="background:transparent; border:1px solid #333; border-radius:12px; padding:1.5rem; height:100%; margin-bottom:1rem;">
        <div style="font-size:1.5rem; margin-bottom:1rem;">{icon}</div>
        <h3 style="font-size:1.1rem; margin-bottom:0.5rem; font-weight:600;">{title}</h3>
        <p style="color:#888; font-size:0.85rem; line-height:1.5; margin:0;">{desc}</p>
    </div>
    """

with f1:
    st.markdown(feature_card("📁", "Project Management", "Organize projects, track progress, manage tasks, and improve team productivity."), unsafe_allow_html=True)
    st.markdown(feature_card("📊", "Analytics Dashboard", "Analytics dashboard creates your analytics and provisions task management."), unsafe_allow_html=True)
with f2:
    st.markdown(feature_card("📋", "Task Tracking", "Organize projects, track progress, manage tasks, and improve team productivity."), unsafe_allow_html=True)
    st.markdown(feature_card("📈", "Progress Monitoring", "Organize projects, track progress, manage tasks, and improve productivity."), unsafe_allow_html=True)
with f3:
    st.markdown(feature_card("👥", "Team Collaboration", "Team collaboration to team collaboration with annotations and encrional areas."), unsafe_allow_html=True)
    st.markdown(feature_card("👤", "Role Based Access", "Role based access allows or necessary project, and role-based access."), unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)

# Dashboard Preview Section / Statistics Section
st.markdown('<h2 style="text-align:center; margin-bottom:1rem;">Statistics Section</h2>', unsafe_allow_html=True)
sc1, sc2, sc3, sc4 = st.columns(4)
with sc1:
    st.markdown('<div style="border:1px solid #333; border-radius:12px; padding:1.5rem; text-align:center;"><p style="color:#888;font-size:0.85rem;margin:0;">Active Projects</p><h2 style="margin:0;font-size:2.5rem;">25</h2></div>', unsafe_allow_html=True)
with sc2:
    st.markdown('<div style="border:1px solid #333; border-radius:12px; padding:1.5rem; text-align:center;"><p style="color:#888;font-size:0.85rem;margin:0;">Completed Tasks</p><h2 style="margin:0;font-size:2.5rem;">1500</h2></div>', unsafe_allow_html=True)
with sc3:
    st.markdown('<div style="border:1px solid #333; border-radius:12px; padding:1.5rem; text-align:center;"><p style="color:#888;font-size:0.85rem;margin:0;">Team Members</p><h2 style="margin:0;font-size:2.5rem;">75</h2></div>', unsafe_allow_html=True)
with sc4:
    st.markdown('<div style="border:1px solid #333; border-radius:12px; padding:1.5rem; text-align:center;"><p style="color:#888;font-size:0.85rem;margin:0;">Productivity Rate</p><h2 style="margin:0;font-size:2.5rem;">92%</h2></div>', unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown('<h2 style="text-align:center; margin-bottom:0.5rem;">Start Managing Your Team Better</h2>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#888; margin-bottom:2rem;">Boost productivity with a clean and efficient task management system.</p>', unsafe_allow_html=True)

cc1, cc2, cc3, cc4 = st.columns([1.5, 1, 1, 1.5])
with cc2:
    if st.button("Create Account", type="primary", use_container_width=True):
        st.switch_page("pages/register.py")
with cc3:
    if st.button("Explore Dashboard", use_container_width=True):
        st.switch_page("pages/login.py")

st.markdown("<br><br><hr style='border-color:#333;'><br>", unsafe_allow_html=True)
fc1, fc2 = st.columns([1, 1])
with fc1:
    st.markdown('<p style="font-size:0.8rem; font-weight:800; color:#fff;">TEAM TASK MANAGER</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.75rem; color:#888;">© 2026 Team Task Manager. All rights reserved.</p>', unsafe_allow_html=True)
with fc2:
    st.markdown('<div style="text-align:right; font-size:0.75rem; color:#888; display:flex; gap:1rem; justify-content:flex-end;"><span>About</span><span>Contact</span><span>Privacy Policy</span><span>Terms</span></div>', unsafe_allow_html=True)
