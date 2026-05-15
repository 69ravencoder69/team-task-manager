import os
from typing import Any, Optional

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


class APIError(Exception):
    def __init__(self, message: str, status_code: int = 0):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def _headers() -> dict:
    headers = {"Content-Type": "application/json"}
    token = st.session_state.get("token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _request(method: str, path: str, **kwargs) -> Any:
    url = f"{API_BASE_URL}{path}"
    try:
        response = requests.request(method, url, headers=_headers(), timeout=30, **kwargs)
    except requests.ConnectionError:
        raise APIError(f"Cannot connect to API at {API_BASE_URL}")

    if response.status_code == 401:
        from utils.session_manager import logout
        logout()
        raise APIError("Session expired. Please log in again.", 401)

    if not response.ok:
        detail = "Request failed"
        try:
            detail = response.json().get("detail", detail)
            if isinstance(detail, list):
                detail = detail[0].get("msg", str(detail))
        except Exception:
            detail = response.text or detail
        raise APIError(str(detail), response.status_code)

    if response.status_code == 204:
        return None
    return response.json()


def register(email: str, password: str, full_name: str, role: Optional[str] = None) -> dict:
    payload = {"email": email, "password": password, "full_name": full_name}
    if role:
        payload["role"] = role
    return _request("POST", "/auth/register", json=payload)


def login(email: str, password: str) -> dict:
    return _request("POST", "/auth/login", json={"email": email, "password": password})


def get_me() -> dict:
    return _request("GET", "/auth/me")


def get_projects() -> list:
    return _request("GET", "/projects")


def create_project(name: str, description: str = "", status: str = "active") -> dict:
    return _request("POST", "/projects", json={"name": name, "description": description, "status": status})


def update_project(project_id: int, **kwargs) -> dict:
    return _request("PUT", f"/projects/{project_id}", json=kwargs)


def delete_project(project_id: int) -> None:
    return _request("DELETE", f"/projects/{project_id}")


def get_project_members(project_id: int) -> list:
    return _request("GET", f"/projects/{project_id}/members")


def add_project_member(project_id: int, user_id: int, role: str = "member") -> dict:
    return _request("POST", f"/projects/{project_id}/members", json={"user_id": user_id, "role": role})


def remove_project_member(project_id: int, user_id: int) -> None:
    return _request("DELETE", f"/projects/{project_id}/members/{user_id}")


def get_tasks(project_id: Optional[int] = None, status: Optional[str] = None, search: Optional[str] = None) -> list:
    params = {}
    if project_id:
        params["project_id"] = project_id
    if status:
        params["status"] = status
    if search:
        params["search"] = search
    return _request("GET", "/tasks", params=params)


def create_task(**kwargs) -> dict:
    return _request("POST", "/tasks", json=kwargs)


def update_task(task_id: int, **kwargs) -> dict:
    return _request("PUT", f"/tasks/{task_id}", json=kwargs)


def delete_task(task_id: int) -> None:
    return _request("DELETE", f"/tasks/{task_id}")


def get_task_comments(task_id: int) -> list:
    return _request("GET", f"/tasks/{task_id}/comments")


def add_task_comment(task_id: int, content: str) -> dict:
    return _request("POST", f"/tasks/{task_id}/comments", json={"content": content})


def get_dashboard_stats() -> dict:
    return _request("GET", "/dashboard/stats")


def get_dashboard_analytics() -> dict:
    return _request("GET", "/dashboard/analytics")


def get_users() -> list:
    return _request("GET", "/users")
