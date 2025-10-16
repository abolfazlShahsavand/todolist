import sys
from src.cli.commands import create_project_cli, list_projects_cli
from src.storage.in_memory import InMemoryStorage
from src.core.services import ProjectService

if __name__ == "__main__":
    print("ToDoList CLI - Starting up...")
    storage = InMemoryStorage()
    service = ProjectService(storage)

    while True:
        print("\n1. Create Project\n2. List Projects\n0. Exit")
        choice = input("Enter your choice (0-2): ")

        if choice == "1":
            create_project_cli(service)
        elif choice == "2":
            list_projects_cli(service)
        elif choice == "0":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice, please try again.")