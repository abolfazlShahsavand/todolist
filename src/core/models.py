from datetime import datetime
from enum import Enum
from typing import List, Optional
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class TaskStatus(Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), unique=True)  # <=30 words ~100 chars
    description: Mapped[str] = mapped_column(String(500))  # <=150 words ~500 chars
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="project", cascade="all, delete-orphan")

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        # Validation (same as Phase 1)
        if len(name.split()) > 30:
            raise ValueError("Name must be <= 30 words")
        if len(description.split()) > 150:
            raise ValueError("Description must be <= 150 words")

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500))
    status: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus), default=TaskStatus.TODO)
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"))

    project: Mapped["Project"] = relationship("Project", back_populates="tasks")

    def __init__(self, title: str, description: str, status: TaskStatus = TaskStatus.TODO, deadline: Optional[datetime] = None):
        self.title = title
        self.description = description
        self.status = status
        self.deadline = deadline
        # Validation
        if len(title.split()) > 30:
            raise ValueError("Title must be <= 30 words")
        if len(description.split()) > 150:
            raise ValueError("Description must be <= 150 words")
        if deadline and deadline < datetime.now():
            raise ValueError("Deadline must be in the future")