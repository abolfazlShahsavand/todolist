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