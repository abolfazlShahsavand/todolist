from src.storage.in_memory import InMemoryStorage
from src.core.models import Project

class ProjectService:
    def __init__(self, storage: InMemoryStorage):
        self.storage = storage

    def create_project(self, name: str, description: str) -> Project:
        project = Project(name=name, description=description)
        self.storage.add_project(project)
        return project

    def list_projects(self):
        return self.storage.get_all_projects()

    def edit_project(self, project_id: str, new_name: str, new_desc: str):
        project = self.storage.get_project(project_id)
        if not project:
            raise ValueError("Project not found")
        project.name = new_name
        project.description = new_desc
        # Manual validation (since no __post_init__)
        if len(project.name.split()) > 30:
            raise ValueError("Name must be <= 30 words")
        if len(project.description.split()) > 150:
            raise ValueError("Description must be <= 150 words")
        self.storage.update_project(project)
    
    def delete_project(self, project_id: str):
        self.storage.delete_project(project_id)


from src.core.models import Task, TaskStatus
from datetime import datetime
from typing import Optional

class TaskService:
    def __init__(self, storage: InMemoryStorage):
        self.storage = storage

    def add_task(self, project_id: str, title: str, description: str, status: str = "todo", deadline: Optional[str] = None):
        try:
            task_status = TaskStatus(status)
        except ValueError:
            raise ValueError("Invalid status")
        dl = datetime.fromisoformat(deadline) if deadline else None
        task = Task(title=title, description=description, status=task_status, deadline=dl)
        self.storage.add_task(project_id, task)
        return task
    def list_tasks(self, project_id: str):
        tasks = self.storage.get_tasks(project_id)
        if not tasks:
            raise ValueError("No tasks or project not found")
        return sorted(tasks, key=lambda t: t.created_at)
    
    def change_status(self, project_id: str, task_id: str, new_status: str):
        try:
            status = TaskStatus(new_status)
        except ValueError:
            raise ValueError("Invalid status")
        task = self.storage.get_task(project_id, task_id)
        if not task:
            raise ValueError("Task not found")
        task.status = status
        self.storage.update_task(project_id, task)
    
    def edit_task(self, project_id: str, task_id: str, new_title: str, new_desc: str, new_deadline: Optional[str], new_status: str):
        task = self.storage.get_task(project_id, task_id)
        if not task:
            raise ValueError("Task not found")
        
        try:
            task_status = TaskStatus(new_status)
        except ValueError:
            raise ValueError("Invalid status")
        
        dl = task.deadline  # نگه داشتن ددلاین قبلی اگه جدید وارد نشه
        if new_deadline:
            try:
                date_str = new_deadline.split(',')[0].strip()
                dl = datetime.fromisoformat(date_str)
                if not (len(date_str.split('-')) == 3 and all(part.isdigit() for part in date_str.split('-'))):
                    raise ValueError("Invalid date format. Use YYYY-MM-DD")
                if dl < datetime.now():
                    raise ValueError("Deadline must be in the future")
            except (ValueError, IndexError):
                raise ValueError("Invalid deadline format. Use ISO format (YYYY-MM-DD, e.g., 2025-02-02)")
        
        # Manual validation
        if len(new_title.split()) > 30:
            raise ValueError("Title must be <= 30 words")
        if len(new_desc.split()) > 150:
            raise ValueError("Description must be <= 150 words")
        
        task.title = new_title
        task.description = new_desc
        task.status = task_status
        task.deadline = dl
        self.storage.update_task(project_id, task)
    
    def delete_task(self, project_id: str, task_id: str):
        self.storage.delete_task(project_id, task_id)
