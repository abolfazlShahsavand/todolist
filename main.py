import sys
from src.cli.commands import create_project_cli
from src.storage.in_memory import InMemoryStorage
from src.core.services import ProjectService

if __name__ == "__main__":
    print("ToDoList CLI - Starting up...")
    storage = InMemoryStorage()
    service = ProjectService(storage)
    create_project_cli(service)
    sys.exit(0)