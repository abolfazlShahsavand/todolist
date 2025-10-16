from typing import Dict, List, Optional
from dotenv import load_dotenv
import os
from src.core.models import Project, Task

load_dotenv()

MAX_PROJECTS = int(os.getenv("MAX_NUMBER_OF_PROJECT", 10))
MAX_TASKS = int(os.getenv("MAX_NUMBER_OF_TASK", 50))


class InMemoryStorage:
    def __init__(self):
        self.projects: Dict[str, Project] = {}

    def add_project(self, project: Project) -> None:
        if len(self.projects) >= MAX_PROJECTS:
            raise ValueError("Max number of projects reached")
        if any(p.name == project.name for p in self.projects.values()):
            raise ValueError("Project name must be unique")
        self.projects[project.id] = project

    def get_project(self, project_id: str) -> Optional[Project]:
        return self.projects.get(project_id)

    def get_all_projects(self) -> List[Project]:
        return sorted(self.projects.values(), key=lambda p: p.created_at)

    def update_project(self, project: Project) -> None:
        if project.id not in self.projects:
            raise ValueError("Project not found")
        if any(p.name == project.name and p.id != project.id for p in self.projects.values()):
            raise ValueError("Project name must be unique")
        self.projects[project.id] = project

    def delete_project(self, project_id: str) -> None:
        if project_id not in self.projects:
            raise ValueError("Project not found")
        del self.projects[project_id]  # Cascade: tasks are in project, so auto-deleted

    def add_task(self, project_id: str, task: Task) -> None:
        project = self.get_project(project_id)
        if not project:
            raise ValueError("Project not found")
        if len(project.tasks) >= MAX_TASKS:
            raise ValueError("Max number of tasks reached")
        project.tasks.append(task)

    def get_tasks(self, project_id: str) -> List[Task]:
        project = self.get_project(project_id)
        return project.tasks if project else []

    def get_task(self, project_id: str, task_id: str) -> Optional[Task]:
        tasks = self.get_tasks(project_id)
        return next((t for t in tasks if t.id == task_id), None)

    def update_task(self, project_id: str, task: Task) -> None:
        old_task = self.get_task(project_id, task.id)
        if not old_task:
            raise ValueError("Task not found")
        tasks = self.get_tasks(project_id)
        index = tasks.index(old_task)
        tasks[index] = task

    def delete_task(self, project_id: str, task_id: str) -> None:
        tasks = self.get_tasks(project_id)
        task = self.get_task(project_id, task_id)
        if not task:
            raise ValueError("Task not found")
        tasks.remove(task)