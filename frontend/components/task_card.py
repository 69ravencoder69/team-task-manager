import streamlit as st

from components.badges import status_badge_html
from utils.theme import get_colors


def render_task_row(task: dict):
    t = get_colors()
    title = task.get("title", "")
    meta = f"{task.get('project_name', '')} / {task.get('assignee_name', 'Unassigned')}"
    badge = status_badge_html(task.get("status", "todo"))
    st.markdown(
        f"""
        <div class="ttm-task-row">
            <div><strong style="color:{t['heading']};">{title}</strong></div>
            <div style="color:{t['muted']};">{meta}</div>
            <div>{badge}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_task_card(task: dict):
    render_task_row(task)
