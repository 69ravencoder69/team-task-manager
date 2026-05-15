import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from components.charts import assignee_bar, priority_bar, status_pie
from components.layout import init_page, navigate_if_needed
from components.navbar import render_navbar
from components.sidebar import render_sidebar
from services import api_service
from services.api_service import APIError
from utils.session_manager import is_admin

st.set_page_config(page_title="Analytics | Team Task Manager", page_icon="⚡", layout="wide")
init_page()

selected = render_sidebar("Analytics")
navigate_if_needed("Analytics", selected)

render_navbar("Analytics", "Team productivity insights" if is_admin() else "Your task analytics")

try:
    analytics = api_service.get_dashboard_analytics()
    stats = api_service.get_dashboard_stats()
except APIError as e:
    st.error(e.message)
    st.stop()

st.markdown('<motion-div class="hover-card">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
c1.metric("Completion Rate", f"{round(stats.get('done_tasks', 0) / max(stats.get('total_tasks', 1), 1) * 100)}%")
c2.metric("In Progress", stats.get("in_progress_tasks", 0))
c3.metric("Overdue", stats.get("overdue_count", 0))
st.markdown("</motion-div>", unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns(2)

with col1:
    fig = status_pie(analytics.get("tasks_by_status", {}))
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No status data yet.")

with col2:
    fig = priority_bar(analytics.get("tasks_by_priority", {}))
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No priority data yet.")

if is_admin() and analytics.get("tasks_by_assignee"):
    st.subheader("Tasks by Team Member")
    fig = assignee_bar(analytics["tasks_by_assignee"])
    if fig:
        st.plotly_chart(fig, use_container_width=True)
