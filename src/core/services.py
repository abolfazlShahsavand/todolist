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