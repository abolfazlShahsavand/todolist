from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional
import uuid


class TaskStatus(Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    status: TaskStatus = TaskStatus.TODO
    deadline: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if len(self.title.split()) > 30:
            raise ValueError("Title must be <= 30 words")
        if len(self.description.split()) > 150:
            raise ValueError("Description must be <= 150 words")
        if self.deadline and self.deadline < datetime.now():
            raise ValueError("Deadline must be in the future")


@dataclass
class Project:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    tasks: List[Task] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if len(self.name.split()) > 30:
            raise ValueError("Name must be <= 30 words")
        if len(self.description.split()) > 150:
            raise ValueError("Description must be <= 150 words")