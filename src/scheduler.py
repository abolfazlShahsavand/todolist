import schedule
import time
from src.storage.repositories import TaskRepository
from src.core.services import TaskService


def run_scheduler():
    task_repo = TaskRepository()
    task_service = TaskService(task_repo)
    schedule.every(1).minutes.do(
        task_service.close_overdue_tasks
    )  # Every minute for testing; change to daily
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run_scheduler()
