# ToDoList Phase 1

A task management (ToDoList) project using Python OOP with in-memory storage in Phase 1.

## Project Status
- Initial setup in progress
- Start Date: October 16, 2025
- Deadline: October 25, 2025 (per documentation)

## Installation and Running
- Installation instructions will be added later.
- Running instructions will be added later.

## Features
- Manage projects and tasks via CLI
- (Features will be detailed later)


# ToDoList Project - Phase 2 (RDB)

## Overview
This is Phase 2 of the ToDoList project for the Software Engineering course at Amirkabir University of Technology (AUT). In this phase, the application transitions from in-memory storage to persistent storage using a Relational Database (PostgreSQL) with SQLAlchemy as the ORM. Key features include:

- Project and Task management via CLI (Create, Read, Update, Delete).
- Cascade deletion (deleting a project removes its tasks).
- Validation for word limits, unique names, status, and deadlines.
- Limits on max projects/tasks loaded from `.env`.
- Auto-closing overdue tasks using a scheduled job (via `schedule` library).
- Database migrations with Alembic.
- Layered architecture: Core (models/services), Storage (repositories), CLI.
- Git workflow with feature branches and develop/main.

The project follows Agile and Incremental Development principles, with User Stories, Functional/Non-Functional Requirements, and Acceptance Criteria as defined in the project docs.

Date: October 2025 (Updated as of December 2025 for maintenance).

## Prerequisites
- Python 3.12+
- Poetry (for dependency management)
- Docker (for PostgreSQL container)
- Git (for version control)

## Setup
1. **Clone the Repository**:
   ```
   git clone https://github.com/abolfazlShahsavand/todolist
   cd todolist-phase2
   ```

2. **Install Dependencies**:
   ```
   poetry install
   ```

3. **Configure Environment Variables**:
   - Copy `.env.example` to `.env` and fill in the values:
     ```
     MAX_NUMBER_OF_PROJECT=10
     MAX_NUMBER_OF_TASK=50
     DB_USER=parsa
     DB_PASSWORD=secret123
     DB_HOST=localhost
     DB_PORT=5432
     DB_NAME=mydb
     ```
   - Ensure `.env` is not committed (it's in `.gitignore`).

4. **Start PostgreSQL with Docker**:
   ```
   docker run --name todolist-db -e POSTGRES_USER=parsa -e POSTGRES_PASSWORD=secret123 -e POSTGRES_DB=mydb -p 5432:5432 -d postgres
   ```
   - Check if running: `docker ps`.
   - Stop/Start: `docker stop todolist-db` / `docker start todolist-db`.

5. **Apply Database Migrations**:
   ```
   poetry run alembic upgrade head
   ```

## Running the Application
### CLI (Main App)
Run the CLI to manage projects and tasks:
```
poetry run python main.py
```
- Menu options: Create/Edit/Delete/List Projects & Tasks, Change Task Status.
- Data persists in PostgreSQL after exit.

### Scheduler (Auto-Close Overdue Tasks)
The scheduler runs periodically to close tasks past their deadline (sets status to "done").

- Run in a separate terminal:
  ```
  poetry run python src/scheduler.py
  ```
- It checks every 1 minute (configurable in code; e.g., change to daily with `schedule.every().day.at("00:00").do(...)`).
- For production, consider using Cron Job: Add to crontab (`crontab -e`):
  ```
  * * * * * /path/to/poetry run python /path/to/project/src/scheduler.py
  ```
- Test: Create a task with a past deadline, wait for the interval, and list tasks to see status updated.

## Testing
- Run unit/integration tests:
  ```
  poetry run pytest
  ```
- For full tests on real DB (including migrations):
  ```
  poetry run test-full
  ```
  (This starts DB if needed, applies migrations, and runs tests.)

## Project Structure
```
todolist-phase2/
├── src/
│   ├── core/
│   │   ├── models.py       # SQLAlchemy models for Project/Task
│   │   └── services.py     # Business logic (ProjectService, TaskService)
│   ├── storage/
│   │   ├── __init__.py     # DB config (DATABASE_URL)
│   │   └── repositories.py # Repository Pattern for DB access
│   ├── cli/
│   │   └── commands.py     # CLI functions
│   └── scheduler.py        # Scheduled task for auto-closing
├── alembic/                # Migrations
├── main.py                 # Entry point for CLI
├── pyproject.toml          # Poetry config
├── .env.example            # Env template
├── README.md               # This file
└── .gitignore
```

## Git Workflow
- Develop on `develop` branch.
- Feature branches: `git checkout -b feature/name`.
- Merge to `develop`, then to `main` for stable releases.
- Commit convention: `feat: ...`, `fix: ...`, `chore: ...`.

## Known Issues / Technical Debt
- In-Memory fallback not implemented (focus on RDB).
- No automated tests for scheduler (manual verification).
- For Phase 3: Add Web API with FastAPI and automated tests.

## Contributors
- Abolfazl (Main developer)

For questions, contact via GitHub issues. This project is for educational purposes.