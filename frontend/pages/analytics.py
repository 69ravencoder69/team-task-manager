import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from components.charts import assignee_bar, priority_bar, status_pie
from components.layout import init_page, navigate_if_needed
from components.page_header import render_page_header
from components.sidebar import render_sidebar
from services import api_service
from services.api_service import APIError
from utils.session_manager import is_admin

st.set_page_config(page_title="Analytics | Team Task Manager", page_icon="⚡", layout="wide")
init_page()

selected = render_sidebar("Analytics")
navigate_if_needed("Analytics", selected)

if not is_admin():
    st.warning("Access denied. Only administrators can view analytics.")
    st.stop()

render_page_header("ANALYTICS", "Team productivity insights")

try:
    analytics = api_service.get_dashboard_analytics()
    stats = api_service.get_dashboard_stats()
except APIError as e:
    st.error(e.message)
    st.stop()

c1, c2, c3 = st.columns(3)
c1.metric("Completion Rate", f"{round(stats.get('done_tasks', 0) / max(stats.get('total_tasks', 1), 1) * 100)}%")
c2.metric("In Progress", stats.get("in_progress_tasks", 0))
c3.metric("Overdue", stats.get("overdue_count", 0))

st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown("### Tasks by Status")
    fig = status_pie(analytics.get("tasks_by_status", {}))
    if fig:
        st.plotly_chart(fig, use_container_width=True)
with col2:
    st.markdown("### Tasks by Priority")
    fig = priority_bar(analytics.get("tasks_by_priority", {}))
    if fig:
        st.plotly_chart(fig, use_container_width=True)

if is_admin() and analytics.get("tasks_by_assignee"):
    st.markdown("### Tasks by Team Member")
    st.caption("Tasks by Assignee")
    fig = assignee_bar(analytics["tasks_by_assignee"])
    if fig:
        st.plotly_chart(fig, use_container_width=True)
