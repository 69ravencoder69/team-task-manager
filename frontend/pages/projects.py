import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from components.layout import init_page, navigate_if_needed
from components.navbar import render_navbar
from components.sidebar import render_sidebar
from services import api_service
from services.api_service import APIError
from utils.session_manager import is_admin
from utils.theme import THEMES, get_theme

st.set_page_config(page_title="Projects | Team Task Manager", page_icon="⚡", layout="wide")
init_page()

selected = render_sidebar("Projects")
navigate_if_needed("Projects", selected)

render_navbar("Projects", "Manage team projects" if is_admin() else "View your projects")

try:
    projects = api_service.get_projects()
except APIError as e:
    st.error(e.message)
    st.stop()

if is_admin():
    with st.expander("➕ Create New Project", expanded=False):
        with st.form("create_project"):
            name = st.text_input("Project Name")
            description = st.text_area("Description")
            status = st.selectbox("Status", ["active", "archived"])
            if st.form_submit_button("Create Project", type="primary"):
                try:
                    api_service.create_project(name, description, status)
                    st.success("Project created!")
                    st.rerun()
                except APIError as e:
                    st.error(e.message)

search = st.text_input("🔍 Search projects", placeholder="Filter by name...")

t = THEMES[get_theme()]
for project in projects:
    if search and search.lower() not in project["name"].lower():
        continue

    st.markdown(
        f"""
        <motion-div class="project-card">
            <h3 style="color:{t['heading']};margin:0 0 8px 0;">📁 {project['name']}</h3>
            <p style="color:{t['muted']};margin:0 0 8px 0;">{project.get('description') or 'No description'}</p>
            <span style="color:{t['text']};font-size:0.9em;">
                Status: <b>{project['status']}</b> ·
                Members: <b>{project.get('member_count', 0)}</b> ·
                Tasks: <b>{project.get('task_count', 0)}</b>
            </span>
        </motion-div>
        """,
        unsafe_allow_html=True,
    )

    if is_admin():
        col1, col2 = st.columns([4, 1])
        with col2:
            with st.popover("⚙️ Manage"):
                if st.button("Delete", key=f"del_{project['id']}", type="secondary"):
                    try:
                        api_service.delete_project(project["id"])
                        st.success("Deleted!")
                        st.rerun()
                    except APIError as e:
                        st.error(e.message)

        with st.expander(f"Members & Settings — {project['name']}"):
            tab1, tab2 = st.tabs(["Members", "Edit"])
            with tab1:
                try:
                    members = api_service.get_project_members(project["id"])
                    for m in members:
                        mc1, mc2 = st.columns([3, 1])
                        mc1.write(f"**{m.get('user_name')}** ({m.get('user_email')}) — {m['role']}")
                        if st.button("Remove", key=f"rm_{project['id']}_{m['user_id']}"):
                            try:
                                api_service.remove_project_member(project["id"], m["user_id"])
                                st.rerun()
                            except APIError as e:
                                st.error(e.message)
                except APIError as e:
                    st.error(e.message)

                st.divider()
                with st.form(f"add_member_{project['id']}"):
                    try:
                        all_users = api_service.get_users()
                        user_options = {f"{u['full_name']} ({u['email']})": u["id"] for u in all_users}
                        selected_user = st.selectbox("Select User", list(user_options.keys()) if user_options else ["No users"])
                        user_id = user_options.get(selected_user, 0)
                    except APIError:
                        user_id = st.number_input("User ID to add", min_value=1, step=1)
                    role = st.selectbox("Role", ["member", "admin"])
                    if st.form_submit_button("Add Member"):
                        try:
                            api_service.add_project_member(project["id"], int(user_id), role)
                            st.success("Member added!")
                            st.rerun()
                        except APIError as e:
                            st.error(e.message)

            with tab2:
                with st.form(f"edit_{project['id']}"):
                    new_name = st.text_input("Name", value=project["name"])
                    new_desc = st.text_area("Description", value=project.get("description") or "")
                    new_status = st.selectbox("Status", ["active", "archived"], index=0 if project["status"] == "active" else 1)
                    if st.form_submit_button("Save Changes"):
                        try:
                            api_service.update_project(project["id"], name=new_name, description=new_desc, status=new_status)
                            st.success("Updated!")
                            st.rerun()
                        except APIError as e:
                            st.error(e.message)

    st.divider()

if not projects:
    st.info("No projects found.")
