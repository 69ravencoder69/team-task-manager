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

st.set_page_config(page_title="Tasks | Team Task Manager", page_icon="⚡", layout="wide")
init_page()
if "task_view" not in st.session_state:
    st.session_state.task_view = "list"

selected = render_sidebar("Tasks")
navigate_if_needed("Tasks", selected)

render_page_header("TASKS", "Manage all the tasks")

st.markdown('<p class="ttm-search-hint">Search Task</p>', unsafe_allow_html=True)
search = st.text_input("task_search", label_visibility="collapsed", placeholder="Search Task")

b1, b2, b3, b4 = st.columns(4)
filter_status = None
with b1:
    if st.button("Create Task  +", use_container_width=True, type="primary"):
        st.session_state.task_view = "create"
with b2:
    if st.button("Filter Task  ⏷", use_container_width=True):
        st.session_state.task_view = "filter"
with b3:
    if st.button("Task Ongoing  ◷", use_container_width=True):
        filter_status = "in_progress"
        st.session_state.task_view = "list"
with b4:
    if st.button("Task Done  ✓", use_container_width=True):
        filter_status = "done"
        st.session_state.task_view = "list"

try:
    projects = api_service.get_projects()
except APIError:
    projects = []

if is_admin() and st.session_state.get("task_view") == "create":
    with st.form("create_task"):
        if projects:
            proj = st.selectbox("Project", projects, format_func=lambda p: p["name"])
            title = st.text_input("Title")
            description = st.text_area("Description")
            priority = st.selectbox("Priority", ["low", "medium", "high"])
            task_status = st.selectbox("Status", ["todo", "in_progress", "done"])
            try:
                users = api_service.get_users()
                opts = {"Unassigned": 0, **{f"{u['full_name']}": u["id"] for u in users}}
                assignee = opts[st.selectbox("Assign To", list(opts.keys()))]
            except APIError:
                assignee = 0
            if st.form_submit_button("Create", type="primary"):
                payload = {"project_id": proj["id"], "title": title, "description": description, "priority": priority, "status": task_status}
                if assignee:
                    payload["assigned_to"] = assignee
                api_service.create_task(**payload)
                st.session_state.task_view = "list"
                st.rerun()

if st.session_state.get("task_view") == "filter":
    fc1, fc2 = st.columns(2)
    with fc1:
        pf = st.selectbox("Project", ["All"] + [p["name"] for p in projects])
    with fc2:
        sf = st.selectbox("Status", ["All", "todo", "in_progress", "done"])

project_id = None
if st.session_state.get("task_view") == "filter" and pf != "All":
    project_id = next((p["id"] for p in projects if p["name"] == pf), None)
if st.session_state.get("task_view") == "filter" and sf != "All":
    filter_status = sf

try:
    tasks = api_service.get_tasks(project_id=project_id, status=filter_status, search=search or None)
except APIError as e:
    st.error(e.message)
    st.stop()

st.markdown("### Task List")
for task in tasks:
    render_task_row(task)
    with st.expander(f"Details — {task['title']}"):
        if is_admin():
            with st.form(f"edit_{task['id']}"):
                nt = st.text_input("Title", value=task["title"])
                ns = st.selectbox("Status", ["todo", "in_progress", "done"], index=["todo", "in_progress", "done"].index(task["status"]))
                np = st.selectbox("Priority", ["low", "medium", "high"], index=["low", "medium", "high"].index(task["priority"]))
                if st.form_submit_button("Update"):
                    api_service.update_task(task["id"], title=nt, status=ns, priority=np)
                    st.rerun()
            if st.button("Delete", key=f"del_{task['id']}"):
                api_service.delete_task(task["id"])
                st.rerun()
        elif task.get("assigned_to") == st.session_state.user.get("id"):
            ns = st.selectbox("Status", ["todo", "in_progress", "done"], index=["todo", "in_progress", "done"].index(task["status"]), key=f"st_{task['id']}")
            if st.button("Save Status", key=f"save_{task['id']}"):
                api_service.update_task(task["id"], status=ns)
                st.rerun()
        try:
            for c in api_service.get_task_comments(task["id"]):
                st.write(f"**{c.get('user_name')}:** {c['content']}")
        except APIError:
            pass
        with st.form(f"cmt_{task['id']}"):
            txt = st.text_input("Comment")
            if st.form_submit_button("Post"):
                api_service.add_task_comment(task["id"], txt)
                st.rerun()

if not tasks:
    st.info("No tasks found.")
