import sys
from src.cli.commands import create_project_cli, list_projects_cli, edit_project_cli, delete_project_cli, add_task_cli,list_tasks_cli, change_status_cli,edit_task_cli,delete_task_cli
from src.storage.in_memory import InMemoryStorage
from src.core.services import ProjectService, TaskService

if __name__ == "__main__":
    print("ToDoList CLI - Starting up...")
    storage = InMemoryStorage()
    service = ProjectService(storage)
    task_service = TaskService(storage)

    while True:
        print("\n1. Create Project\n2. List Projects\n3. Edit Project\n4. Delete Projects\n5. Add Task\n6. List Task\n7. Change status Task\n8. Edit Task\n0. Exit")
        choice = input("Enter your choice (0-5): ")

        if choice == "1":
            create_project_cli(service)
        elif choice == "2":
            list_projects_cli(service)
        elif choice == "3":
            edit_project_cli(service)
        elif choice == "4":
            delete_project_cli(service)
        elif choice == "5":
            add_task_cli(task_service)
        elif choice == "6":
            list_tasks_cli(task_service)
        elif choice == "7":
            change_status_cli(task_service)
        elif choice == "8":
            edit_task_cli(task_service)
        elif choice == "9":
            delete_task_cli(task_service)
        elif choice == "0":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice, please try again.")