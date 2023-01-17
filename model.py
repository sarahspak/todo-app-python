from datetime import datetime


class Todo:
    def __init__(self, task: str, category: str, date_added=None, date_completed=None, status=None, position=None):
        self.task = task
        self.category = category
        self.date_added = date_added if date_added is not None else datetime.now().isoformat()
        self.date_completed = date_completed
        self.status = status if status is not None else 0  # 1 = completed, 0 = not completed
        self.position = position

    def __repr__(self) -> str:
        """Return a string representation of the Todo object."""
        return f"{self.task} - {self.category} - {self.date_added} - {self.date_completed} - {self.status}"
