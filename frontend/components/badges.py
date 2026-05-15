def status_badge_html(status: str) -> str:
    s = (status or "todo").replace("_", " ")
    label = s.title()
    if status == "done":
        cls = "ttm-badge-done"
    elif status == "in_progress":
        cls = "ttm-badge-progress"
    else:
        cls = "ttm-badge-todo"
    return f'<span class="ttm-badge {cls}">{label}</span>'
