from datetime import datetime
from enum import Enum
from typing import List, Optional
import uuid


class TaskStatus(Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class Task:
    def __init__(
        self,
        title: str,
        description: str,
        status: TaskStatus = TaskStatus.TODO,
        deadline: Optional[datetime] = None,
    ):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.status = status
        self.deadline = deadline
        self.created_at = datetime.now()

        # Validation (مثل همون‌هایی که توی __post_init__ بود)
        if len(self.title.split()) > 30:
            raise ValueError("Title must be <= 30 words")
        if len(self.description.split()) > 150:
            raise ValueError("Description must be <= 150 words")
        if self.deadline and self.deadline < datetime.now():
            raise ValueError("Deadline must be in the future")


class Project:
    def __init__(self, name: str, description: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.tasks: List[Task] = []
        self.created_at = datetime.now()

        # Validation
        if len(self.name.split()) > 30:
            raise ValueError("Name must be <= 30 words")
        if len(self.description.split()) > 150:
            raise ValueError("Description must be <= 150 words")
