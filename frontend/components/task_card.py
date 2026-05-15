import streamlit as st

from utils.theme import THEMES, get_theme

STATUS_COLORS = {
    "todo": "#FFA726",
    "in_progress": "#42A5F5",
    "done": "#66BB6A",
}

PRIORITY_ICONS = {"low": "🟢", "medium": "🟡", "high": "🔴"}


def render_task_card(task: dict):
    status = task.get("status", "todo")
    color = STATUS_COLORS.get(status, "#888")
    priority_icon = PRIORITY_ICONS.get(task.get("priority", "medium"), "🟡")
    t = THEMES[get_theme()]
    title_color = t["heading"]
    muted = t["muted"]

    st.markdown(
        f"""
        <motion-div class="task-card-hover" style="border-left: 4px solid {color};">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <strong style="color:{title_color};font-size:1.1em;">{task.get('title','')}</strong>
                <span>{priority_icon}</span>
            </motion-div>
            <p style="color:{muted};margin:8px 0 0 0;font-size:0.9em;">
                {task.get('project_name','')} · {task.get('assignee_name','Unassigned')}
            </p>
            <span style="
                background:{color}33;
                color:{color};
                padding:2px 10px;
                border-radius:12px;
                font-size:0.8em;
            ">{status.replace('_',' ').title()}</span>
        </motion-div>
        """,
        unsafe_allow_html=True,
    )
