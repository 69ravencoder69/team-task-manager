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

# ── handle nav query-param redirects ──────────────────────────────────────────
params = st.query_params
nav_action = params.get("nav", None)

if nav_action == "features":
    # clear param then rerun so page loads fresh; JS scroll handled below
    st.query_params.clear()
elif nav_action in ("dashboard", "projects", "analytics"):
    # Store intended destination in session and send to login
    st.session_state["post_login_redirect"] = f"pages/{nav_action}.py"
    st.query_params.clear()
    st.switch_page("pages/login.py")

# ── Hide sidebar ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebar"]        { display: none !important; }

/* ── Nav link buttons ──────────────────────────────────────────────────────── */
.nav-link-btn button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #888 !important;
    font-size: 0.85rem !important;
    padding: 0.3rem 0.6rem !important;
    min-height: 0 !important;
    border-radius: 6px !important;
    transition: color 0.2s ease, background 0.2s ease !important;
}
.nav-link-btn button:hover {
    color: #fff !important;
    background: rgba(255,255,255,0.07) !important;
}
.nav-link-btn button p { margin: 0 !important; font-size: 0.85rem !important; }

/* ── Top-right Login button ─────────────────────────────────────────────────── */
.nav-login-btn button {
    background: transparent !important;
    border: 1px solid #555 !important;
    box-shadow: none !important;
    color: #ccc !important;
    font-size: 0.85rem !important;
    padding: 0.3rem 1rem !important;
    min-height: 0 !important;
    border-radius: 6px !important;
    transition: background 0.2s ease, border-color 0.2s ease, color 0.2s ease !important;
}
.nav-login-btn button:hover {
    background: #fff !important;
    border-color: #fff !important;
    color: #000 !important;
}
.nav-login-btn button p { margin: 0 !important; }

/* ── Hero CTA buttons ───────────────────────────────────────────────────────── */
.hero-btn-primary button {
    background: #fff !important;
    border: none !important;
    color: #000 !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.2rem !important;
    font-size: 0.9rem !important;
    transition: background 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease !important;
    box-shadow: 0 2px 8px rgba(255,255,255,0.15) !important;
}
.hero-btn-primary button:hover {
    background: #e0e0e0 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(255,255,255,0.2) !important;
}
.hero-btn-secondary button {
    background: transparent !important;
    border: 1px solid #555 !important;
    color: #ccc !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.2rem !important;
    font-size: 0.9rem !important;
    transition: background 0.2s ease, border-color 0.2s ease, color 0.2s ease, transform 0.15s ease !important;
}
.hero-btn-secondary button:hover {
    background: rgba(255,255,255,0.08) !important;
    border-color: #aaa !important;
    color: #fff !important;
    transform: translateY(-2px) !important;
}
.hero-btn-primary button p,
.hero-btn-secondary button p { margin: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Top Nav ────────────────────────────────────────────────────────────────────
nav_c1, n1, n2, n3, n4, n5, nav_c3 = st.columns([2.5, 0.9, 0.9, 1.1, 0.9, 1.1, 1])

with nav_c1:
    st.markdown(
        '<div style="font-weight:800; font-size:1.2rem; letter-spacing:0.02em; '
        'padding-top:0.5rem; text-transform:uppercase;">TEAM TASK MANAGER</div>',
        unsafe_allow_html=True,
    )

with n1:
    st.markdown('<div class="nav-link-btn">', unsafe_allow_html=True)
    if st.button("Home", key="nav_home", use_container_width=True):
        st.query_params.clear()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with n2:
    st.markdown('<div class="nav-link-btn">', unsafe_allow_html=True)
    if st.button("Features", key="nav_features", use_container_width=True):
        st.query_params["nav"] = "features"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with n3:
    st.markdown('<div class="nav-link-btn">', unsafe_allow_html=True)
    if st.button("Dashboard", key="nav_dashboard", use_container_width=True):
        st.session_state["post_login_redirect"] = "pages/dashboard.py"
        st.switch_page("pages/login.py")
    st.markdown('</div>', unsafe_allow_html=True)

with n4:
    st.markdown('<div class="nav-link-btn">', unsafe_allow_html=True)
    if st.button("Projects", key="nav_projects", use_container_width=True):
        st.session_state["post_login_redirect"] = "pages/projects.py"
        st.switch_page("pages/login.py")
    st.markdown('</div>', unsafe_allow_html=True)

with n5:
    st.markdown('<div class="nav-link-btn">', unsafe_allow_html=True)
    if st.button("Analytics", key="nav_analytics", use_container_width=True):
        st.session_state["post_login_redirect"] = "pages/analytics.py"
        st.switch_page("pages/login.py")
    st.markdown('</div>', unsafe_allow_html=True)

with nav_c3:
    st.markdown('<div class="nav-login-btn">', unsafe_allow_html=True)
    if st.button("Login", key="top_login", use_container_width=True):
        st.switch_page("pages/login.py")
    st.markdown('</div>', unsafe_allow_html=True)

# ── Features anchor (JS scroll when ?nav=features) ────────────────────────────
st.markdown("""
<script>
const params = new URLSearchParams(window.location.search);
if (params.get('nav') === 'features') {
    setTimeout(() => {
        const el = document.getElementById('features-section');
        if (el) el.scrollIntoView({behavior: 'smooth'});
    }, 600);
}
</script>
""", unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)

# ── Hero Section ───────────────────────────────────────────────────────────────
st.markdown(
    '<h1 style="font-size:3.5rem; font-weight:800; line-height:1.1; margin-bottom:1rem;">'
    'Manage Your Team<br>Tasks Efficiently</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p style="color:#888; font-size:1.1rem; line-height:1.6; margin-bottom:2rem;">'
    'Organize projects, track progress, manage tasks, and improve team productivity '
    'from one simple dashboard.</p>',
    unsafe_allow_html=True,
)

bc1, bc2, bc3 = st.columns([1, 1, 6])
with bc1:
    st.markdown('<div class="hero-btn-primary">', unsafe_allow_html=True)
    if st.button("Get Started", key="hero_getstarted", use_container_width=True):
        st.switch_page("pages/register.py")
    st.markdown('</div>', unsafe_allow_html=True)
with bc2:
    st.markdown('<div class="hero-btn-secondary">', unsafe_allow_html=True)
    if st.button("Login", key="hero_login", use_container_width=True):
        st.switch_page("pages/login.py")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><br><br><br>", unsafe_allow_html=True)

# ── Features Section ───────────────────────────────────────────────────────────
st.markdown('<div id="features-section"></div>', unsafe_allow_html=True)
st.markdown('<h2 style="text-align:center; margin-bottom:3rem;">Features</h2>', unsafe_allow_html=True)
f1, f2, f3 = st.columns(3)

def feature_card(icon, title, desc):
    return f"""
    <div style="background:transparent; border:1px solid #333; border-radius:12px;
                padding:1.5rem; height:100%; margin-bottom:1rem;
                transition:border-color 0.2s ease;">
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

# ── Statistics Section ─────────────────────────────────────────────────────────
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
