from src.core.services import ProjectService, TaskService


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


def edit_project_cli(service: ProjectService):
    pid = input("Enter project ID: ")
    name = input("New name: ")
    desc = input("New desc: ")
    try:
        service.edit_project(pid, name, desc)
        print("Project edited.")
    except ValueError as e:
        print(f"Error: {e}")


def delete_project_cli(service: ProjectService):
    pid = input("Enter project ID to delete: ")
    confirm = input("Confirm (y/n): ")
    if confirm.lower() == "y":
        try:
            service.delete_project(pid)
            print("Project deleted.")
        except ValueError as e:
            print(f"Error: {e}")
    else:
        print("Deletion cancelled.")


def add_task_cli(task_service: TaskService):
    pid = input("Project ID: ")
    title = input("Title: ")
    desc = input("Desc: ")
    status = input("Status (todo/doing/done, default todo): ") or "todo"
    dl = input("Deadline (YYYY-MM-DD, optional): ")
    try:
        task = task_service.add_task(pid, title, desc, status, dl)
        print(f"Task added: {task.id}")
    except ValueError as e:
        print(f"Error: {e}")


def list_tasks_cli(task_service: TaskService):
    pid = input("Project ID: ")
    try:
        tasks = task_service.list_tasks(pid)
        for t in tasks:
            dl = t.deadline.isoformat() if t.deadline else "None"
            print(
                f"ID: {t.id}, Title: {t.title}, Status: {t.status.value}, \
                    Deadline: {dl}"
            )
    except ValueError as e:
        print(f"Error: {e}")


def change_status_cli(task_service: TaskService):
    pid = input("Project ID: ")
    tid = input("Task ID: ")
    status = input("New status (todo/doing/done): ")
    try:
        task_service.change_status(pid, tid, status)
        print("Status changed.")
    except ValueError as e:
        print(f"Error: {e}")


def edit_task_cli(task_service: TaskService):
    pid = input("Project ID: ")
    tid = input("Task ID: ")
    title = input("New title: ")
    desc = input("New desc: ")
    status = input("New status: ")
    dl = input("New deadline (optional): ")
    try:
        task_service.edit_task(pid, tid, title, desc, dl, status)
        print("Task edited.")
    except ValueError as e:
        print(f"Error: {e}")


def delete_task_cli(task_service: TaskService):
    pid = input("Project ID: ")
    tid = input("Task ID to delete: ")
    confirm = input("Confirm (y/n): ")
    if confirm.lower() == "y":
        try:
            task_service.delete_task(pid, tid)
            print("Task deleted.")
        except ValueError as e:
            print(f"Error: {e}")
