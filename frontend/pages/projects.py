import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from components.layout import init_page, navigate_if_needed
from components.page_header import render_page_header
from components.sidebar import render_sidebar
from services import api_service
from services.api_service import APIError
from utils.session_manager import is_admin
from utils.theme import get_colors

st.set_page_config(page_title="Projects | Team Task Manager", page_icon="⚡", layout="wide")
init_page()

selected = render_sidebar("Projects")
navigate_if_needed("Projects", selected)

render_page_header("PROJECTS", "Manage Project")

if is_admin():
    if st.button("Create New Project  +", type="primary"):
        st.session_state.show_create_project = True
    if st.session_state.get("show_create_project"):
        with st.form("create_project"):
            name = st.text_input("Project Name")
            description = st.text_area("Description")
            status = st.selectbox("Status", ["active", "archived"])
            if st.form_submit_button("Create", type="primary"):
                try:
                    api_service.create_project(name, description, status)
                    st.session_state.show_create_project = False
                    st.success("Project created!")
                    st.rerun()
                except APIError as e:
                    st.error(e.message)

st.markdown('<p class="ttm-search-hint">Search Projects</p>', unsafe_allow_html=True)
search = st.text_input("search", label_visibility="collapsed", placeholder="Filter by name...")

try:
    projects = api_service.get_projects()
except APIError as e:
    st.error(e.message)
    st.stop()

t = get_colors()
for project in projects:
    if search and search.lower() not in project["name"].lower():
        continue

    status_label = project["status"].title() if isinstance(project["status"], str) else str(project["status"])
    st.markdown(
        f"""
        <div class="ttm-project-row">
            <div style="font-size:2rem;color:{t['heading']};margin-right:1rem;">📁</div>
            <div>
                <h3 style="color:{t['heading']};margin:0;font-size:1.1rem;font-weight:600;">{project['name']}</h3>
                <p style="color:{t['muted']};margin:0.2rem 0 0 0;font-size:0.85rem;">{project.get('description') or 'No description'}</p>
            </div>
            <div><span style="color:{t['muted']};font-size:0.75rem;">Status</span><br><span class="ttm-badge" style="background:#333;color:#ccc;margin-top:0.2rem;">{status_label}</span></div>
            <div><span style="color:{t['muted']};font-size:0.75rem;">Members</span><br><b style="font-size:1.1rem;color:{t['heading']};">{project.get('member_count', 0)}</b></div>
            <div><span style="color:{t['muted']};font-size:0.75rem;">Tasks</span><br><b style="font-size:1.1rem;color:{t['heading']};">{project.get('task_count', 0)}</b></div>
            <div><button style="background:transparent;border:1px solid {t['border']};border-radius:4px;color:{t['text']};padding:0.25rem 0.75rem;cursor:pointer;">Manage ˅</button></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if is_admin():
        with st.expander(f"Members & Settings — {project['name']}"):
            try:
                members = api_service.get_project_members(project["id"])
                for m in members:
                    c1, c2 = st.columns([4, 1])
                    c1.write(f"**{m.get('user_name')}** ({m.get('user_email')}) — {m['role']}")
                    if c2.button("Remove", key=f"rm_{project['id']}_{m['user_id']}"):
                        api_service.remove_project_member(project["id"], m["user_id"])
                        st.rerun()
            except APIError as e:
                st.error(e.message)

            with st.form(f"add_member_{project['id']}"):
                try:
                    all_users = api_service.get_users()
                    user_options = {f"{u['full_name']} ({u['email']})": u["id"] for u in all_users}
                    sel = st.selectbox("Select User", list(user_options.keys()))
                    user_id = user_options.get(sel, 0)
                except APIError:
                    user_id = st.number_input("User ID", min_value=1, step=1)
                role = st.selectbox("Role", ["member", "admin"])
                if st.form_submit_button("Add Member"):
                    api_service.add_project_member(project["id"], int(user_id), role)
                    st.rerun()

            with st.form(f"edit_{project['id']}"):
                new_name = st.text_input("Name", value=project["name"])
                new_desc = st.text_area("Description", value=project.get("description") or "")
                new_status = st.selectbox("Status", ["active", "archived"], index=0 if project["status"] == "active" else 1)
                c1, c2 = st.columns(2)
                if c1.form_submit_button("Save"):
                    api_service.update_project(project["id"], name=new_name, description=new_desc, status=new_status)
                    st.rerun()
                if c2.form_submit_button("Delete Project"):
                    api_service.delete_project(project["id"])
                    st.rerun()

if not projects:
    st.info("No projects found.")
