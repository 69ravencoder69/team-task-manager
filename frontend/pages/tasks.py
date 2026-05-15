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

st.set_page_config(page_title="Tasks | Team Task Manager", page_icon="⚡", layout="wide")
init_page()

selected = render_sidebar("Tasks")
navigate_if_needed("Tasks", selected)

render_navbar("Tasks", "Manage and track team tasks")

try:
    projects = api_service.get_projects()
except APIError:
    projects = []

with st.expander("🔍 Filters", expanded=True):
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        project_filter = st.selectbox("Project", ["All"] + [p["name"] for p in projects])
    with fc2:
        status_filter = st.selectbox("Status", ["All", "todo", "in_progress", "done"])
    with fc3:
        search = st.text_input("Search", placeholder="Search by title...")

project_id = None
if project_filter != "All":
    project_id = next((p["id"] for p in projects if p["name"] == project_filter), None)

status = status_filter if status_filter != "All" else None

if is_admin():
    with st.expander("➕ Create New Task"):
        with st.form("create_task"):
            if not projects:
                st.warning("Create a project first.")
            else:
                proj = st.selectbox("Project", projects, format_func=lambda p: p["name"])
                title = st.text_input("Title")
                description = st.text_area("Description")
                priority = st.selectbox("Priority", ["low", "medium", "high"])
                task_status = st.selectbox("Status", ["todo", "in_progress", "done"])
                try:
                    all_users = api_service.get_users()
                    user_options = {"Unassigned": 0}
                    user_options.update({f"{u['full_name']} ({u['email']})": u["id"] for u in all_users})
                    selected_assignee = st.selectbox("Assign To", list(user_options.keys()))
                    assigned_to = user_options[selected_assignee]
                except APIError:
                    assigned_to = st.number_input("Assign to User ID", min_value=0, step=1, value=0)
                due = st.date_input("Due Date", value=None)
                if st.form_submit_button("Create Task", type="primary"):
                    try:
                        payload = {
                            "project_id": proj["id"],
                            "title": title,
                            "description": description,
                            "priority": priority,
                            "status": task_status,
                        }
                        if assigned_to > 0:
                            payload["assigned_to"] = int(assigned_to)
                        if due:
                            payload["due_date"] = str(due)
                        api_service.create_task(**payload)
                        st.success("Task created!")
                        st.rerun()
                    except APIError as e:
                        st.error(e.message)

try:
    tasks = api_service.get_tasks(
        project_id=project_id,
        status=status,
        search=search if search else None,
    )
except APIError as e:
    st.error(e.message)
    st.stop()

for task in tasks:
    render_task_card(task)

    with st.expander(f"Details: {task['title']}"):
        if is_admin():
            with st.form(f"edit_task_{task['id']}"):
                new_title = st.text_input("Title", value=task["title"], key=f"t_{task['id']}")
                new_status = st.selectbox("Status", ["todo", "in_progress", "done"], index=["todo", "in_progress", "done"].index(task["status"]), key=f"s_{task['id']}")
                new_priority = st.selectbox("Priority", ["low", "medium", "high"], index=["low", "medium", "high"].index(task["priority"]), key=f"p_{task['id']}")
                if st.form_submit_button("Update Task"):
                    try:
                        api_service.update_task(task["id"], title=new_title, status=new_status, priority=new_priority)
                        st.success("Updated!")
                        st.rerun()
                    except APIError as e:
                        st.error(e.message)

            if st.button("Delete Task", key=f"del_task_{task['id']}"):
                try:
                    api_service.delete_task(task["id"])
                    st.success("Deleted!")
                    st.rerun()
                except APIError as e:
                    st.error(e.message)
        else:
            if task.get("assigned_to") == st.session_state.user.get("id"):
                new_status = st.selectbox(
                    "Update Status",
                    ["todo", "in_progress", "done"],
                    index=["todo", "in_progress", "done"].index(task["status"]),
                    key=f"ms_{task['id']}",
                )
                if st.button("Save Status", key=f"save_{task['id']}"):
                    try:
                        api_service.update_task(task["id"], status=new_status)
                        st.success("Status updated!")
                        st.rerun()
                    except APIError as e:
                        st.error(e.message)
            else:
                st.caption("You can only update tasks assigned to you.")

        st.subheader("Comments")
        try:
            comments = api_service.get_task_comments(task["id"])
            for c in comments:
                st.markdown(f"**{c.get('user_name', 'User')}:** {c['content']}")
                st.caption(str(c.get("created_at", ""))[:19])
        except APIError:
            pass

        with st.form(f"comment_{task['id']}"):
            content = st.text_input("Add a comment", key=f"c_{task['id']}")
            if st.form_submit_button("Post Comment"):
                try:
                    api_service.add_task_comment(task["id"], content)
                    st.success("Comment added!")
                    st.rerun()
                except APIError as e:
                    st.error(e.message)

    st.divider()

if not tasks:
    st.info("No tasks match your filters.")
