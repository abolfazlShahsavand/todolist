from src.core.services import ProjectService
from src.storage.in_memory import InMemoryStorage


def create_project_cli(service: ProjectService):
    name = input("Enter project name: ")
    desc = input("Enter project description: ")
    try:
        project = service.create_project(name, desc)
        print(f"Project created: {project.id}")
    except ValueError as e:
        print(f"Error: {e}")
    
def list_projects_cli(service: ProjectService):
    projects = service.list_projects()
    if not projects:
        print("No projects exist.")
        return
    for p in projects:
        print(f"ID: {p.id}, Name: {p.name}, Desc: {p.description}")