from datetime import datetime
from typing import Optional

from src.storage.repositories import ProjectRepository, TaskRepository
from src.core.models import Project, Task, TaskStatus
from src.storage.repositories import SessionLocal

# ===========================
#      PROJECT SERVICE
# ===========================

class ProjectService:
    def __init__(self, repo: ProjectRepository):
        self.repo = repo

    def create_project(self, name: str, description: str) -> Project:
        project = Project(name=name, description=description)
        self.repo.add_project(project)
        return project

    def list_projects(self):
        return self.repo.get_all_projects()

    def edit_project(self, project_id: str, new_name: str, new_desc: str):
        project = self.repo.get_project(project_id)
        if not project:
            raise ValueError("Project not found")

        # Validation
        if len(new_name.split()) > 30:
            raise ValueError("Name must be <= 30 words")
        if len(new_desc.split()) > 150:
            raise ValueError("Description must be <= 150 words")

        project.name = new_name
        project.description = new_desc

        self.repo.update_project(project)

    def delete_project(self, project_id: str):
        self.repo.delete_project(project_id)


# ===========================
#        TASK SERVICE
# ===========================

class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def add_task(
        self,
        project_id: str,
        title: str,
        description: str,
        status: str = "todo",
        deadline: Optional[str] = None,
    ) -> Task:
        try:
            task_status = TaskStatus(status)
        except ValueError:
            raise ValueError("Invalid status")

        dl = datetime.fromisoformat(deadline) if deadline else None

        task = Task(
            title=title,
            description=description,
            status=task_status,
            deadline=dl,
        )

        self.repo.add_task(project_id, task)
        return task

    def list_tasks(self, project_id: str):
        tasks = self.repo.get_tasks(project_id)
        if not tasks:
            raise ValueError("No tasks or project not found")
        return sorted(tasks, key=lambda t: t.created_at)

    def change_status(self, project_id: str, task_id: str, new_status: str):
        try:
            status = TaskStatus(new_status)
        except ValueError:
            raise ValueError("Invalid status")

        task = self.repo.get_task(project_id, task_id)
        if not task:
            raise ValueError("Task not found")

        task.status = status
        self.repo.update_task(task)

    def edit_task(
        self,
        project_id: str,
        task_id: str,
        new_title: str,
        new_desc: str,
        new_deadline: Optional[str],
        new_status: str,
    ):
        task = self.repo.get_task(project_id, task_id)
        if not task:
            raise ValueError("Task not found")

        # Status validatiomust be in n
        try:
            status = TaskStatus(new_status)
        except ValueError:
            raise ValueError("Invalid status")

        # Deadline parsing
        dl = task.deadline
        if new_deadline:
            try:
                date_str = new_deadline.split(",")[0].strip()
                dl = datetime.fromisoformat(date_str)

                # Check proper format
                if not (
                    len(date_str.split("-")) == 3
                    and all(part.isdigit() for part in date_str.split("-"))
                ):
                    raise ValueError("Invalid date format. Use YYYY-MM-DD")

                if dl < datetime.now():
                    raise ValueError("Deadline must be in the future")
            except (ValueError, IndexError):
                raise ValueError(
                    "Invalid deadline format. Use ISO format (YYYY-MM-DD)"
                )

        # Title & description validation
        if len(new_title.split()) > 30:
            raise ValueError("Title must be <= 30 words")
        if len(new_desc.split()) > 150:
            raise ValueError("Description must be <= 150 words")

        task.title = new_title
        task.description = new_desc
        task.status = status
        task.deadline = dl

        self.repo.update_task(task)

    def delete_task(self, project_id: str, task_id: str):
        self.repo.delete_task(project_id, task_id)

    from datetime import datetime

    def close_overdue_tasks(self):
        with SessionLocal() as session:  # Assume imported
            overdue = session.query(Task).filter(Task.deadline < datetime.now(), Task.status != TaskStatus.DONE).all()
            for task in overdue:
                task.status = TaskStatus.DONE
            session.commit()
            return len(overdue)     
