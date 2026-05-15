import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from components.layout import init_page, navigate_if_needed
from components.page_header import render_page_header
from components.sidebar import render_sidebar
from components.task_card import render_task_row
from services import api_service
from services.api_service import APIError
from utils.session_manager import is_admin

st.set_page_config(page_title="Dashboard | Team Task Manager", page_icon="⚡", layout="wide")
init_page()

selected = render_sidebar("Dashboard")
navigate_if_needed("Dashboard", selected)

render_page_header("DASHBOARD", "Overview of your team's progress")

try:
    stats = api_service.get_dashboard_stats()
except APIError as e:
    st.error(e.message)
    st.stop()

if stats.get("overdue_count", 0) > 0:
    st.warning(f"{stats['overdue_count']} task(s) are overdue.")

r1 = st.columns(4)
labels1 = ["Total Projects", "Active Projects", "Total Tasks", "My Open Tasks"]
keys1 = ["total_projects", "active_projects", "total_tasks", "my_open_tasks"]
for col, label, key in zip(r1, labels1, keys1):
    with col:
        st.metric(label, stats.get(key, 0))

r2 = st.columns(4)
labels2 = ["To Do", "In Progress", "Done", "Overdue"]
keys2 = ["todo_tasks", "in_progress_tasks", "done_tasks", "overdue_count"]
for col, label, key in zip(r2, labels2, keys2):
    with col:
        st.metric(label, stats.get(key, 0))

st.markdown("### Recent Tasks")
try:
    tasks = api_service.get_tasks()
    for task in tasks[:8]:
        render_task_row(task)
    if not tasks:
        st.info("No tasks yet." if not is_admin() else "Create tasks from the TASK page.")
except APIError as e:
    st.error(e.message)
