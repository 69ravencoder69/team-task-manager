import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from components.layout import init_page, navigate_if_needed
from components.navbar import render_navbar
from components.sidebar import render_sidebar
from components.task_card import render_task_card
from services import api_service
from services.api_service import APIError
from utils.session_manager import is_admin

st.set_page_config(page_title="Dashboard | Team Task Manager", page_icon="⚡", layout="wide")
init_page()

selected = render_sidebar("Dashboard")
navigate_if_needed("Dashboard", selected)

render_navbar("Dashboard", "Overview of your team's progress")

try:
    stats = api_service.get_dashboard_stats()
except APIError as e:
    st.error(e.message)
    st.stop()

if stats.get("overdue_count", 0) > 0:
    st.warning(f"⚠️ {stats['overdue_count']} task(s) are overdue!")

st.markdown('<motion-div class="hover-card">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Projects", stats.get("total_projects", 0))
c2.metric("Active Projects", stats.get("active_projects", 0))
c3.metric("Total Tasks", stats.get("total_tasks", 0))
c4.metric("My Open Tasks", stats.get("my_open_tasks", 0))
st.markdown("</motion-div>", unsafe_allow_html=True)

st.divider()

c5, c6, c7, c8 = st.columns(4)
c5.metric("To Do", stats.get("todo_tasks", 0))
c6.metric("In Progress", stats.get("in_progress_tasks", 0))
c7.metric("Done", stats.get("done_tasks", 0))
c8.metric("Overdue", stats.get("overdue_count", 0))

st.divider()
st.subheader("Recent Tasks")

try:
    tasks = api_service.get_tasks()
    for task in tasks[:6]:
        render_task_card(task)
    if not tasks:
        st.info("No tasks yet. " + ("Create some from the Tasks page!" if is_admin() else "Tasks will appear when assigned to you."))
except APIError as e:
    st.error(e.message)
