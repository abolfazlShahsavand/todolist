from typing import List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from src.storage import DATABASE_URL
from src.core.models import Project, Task, TaskStatus
import os
from dotenv import load_dotenv

load_dotenv()
MAX_PROJECTS = int(os.getenv("MAX_NUMBER_OF_PROJECT", 10))
MAX_TASKS = int(os.getenv("MAX_NUMBER_OF_TASK", 50))

engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

class ProjectRepository:
    def add_project(self, project: Project) -> None:
        with SessionLocal() as session:
            if session.query(Project).count() >= MAX_PROJECTS:
                raise ValueError("Max number of projects reached")
            if session.query(Project).filter_by(name=project.name).first():
                raise ValueError("Project name must be unique")
            session.add(project)
            session.commit()
            session.refresh(project)

    def get_project(self, project_id: str) -> Optional[Project]:
        with SessionLocal() as session:
            return session.query(Project).filter_by(id=project_id).first()

    def get_all_projects(self) -> List[Project]:
        with SessionLocal() as session:
            return session.query(Project).order_by(Project.created_at).all()

    def update_project(self, project: Project) -> None:
        with SessionLocal() as session:
            existing = session.query(Project).filter_by(id=project.id).first()
            if not existing:
                raise ValueError("Project not found")
            if session.query(Project).filter(Project.name == project.name, Project.id != project.id).first():
                raise ValueError("Project name must be unique")
            existing.name = project.name
            existing.description = project.description
            session.commit()

    def delete_project(self, project_id: str) -> None:
        with SessionLocal() as session:
            project = session.query(Project).filter_by(id=project_id).first()
            if not project:
                raise ValueError("Project not found")
            session.delete(project)
            session.commit()  # Cascade deletes tasks

class TaskRepository:
    def add_task(self, project_id: str, task: Task) -> None:
        with SessionLocal() as session:
            project = session.query(Project).filter_by(id=project_id).first()
            if not project:
                raise ValueError("Project not found")
            if len(project.tasks) >= MAX_TASKS:
                raise ValueError("Max number of tasks reached")
            task.project_id = project_id
            session.add(task)
            session.commit()
            session.refresh(task)

    def get_tasks(self, project_id: str) -> List[Task]:
        with SessionLocal() as session:
            return session.query(Task).filter_by(project_id=project_id).order_by(Task.created_at).all()

    def get_task(self, project_id: str, task_id: str) -> Optional[Task]:
        with SessionLocal() as session:
            return session.query(Task).filter_by(id=task_id, project_id=project_id).first()

    def update_task(self, task: Task) -> None:
        with SessionLocal() as session:
            existing = session.query(Task).filter_by(id=task.id).first()
            if not existing:
                raise ValueError("Task not found")
            existing.title = task.title
            existing.description = task.description
            existing.status = task.status
            existing.deadline = task.deadline
            session.commit()

    def delete_task(self, project_id: str, task_id: str) -> None:
        with SessionLocal() as session:
            task = session.query(Task).filter_by(id=task_id, project_id=project_id).first()
            if not task:
                raise ValueError("Task not found")
            session.delete(task)
            session.commit()