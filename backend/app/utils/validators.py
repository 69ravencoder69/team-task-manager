def is_overdue(due_date, status: str) -> bool:
    if due_date is None or status == "done":
        return False
    from datetime import date

    return due_date < date.today()
