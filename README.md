# Task Management System
> Django-based team task management application

A comprehensive task management system built with Django that enables teams to organize work efficiently,
track task progress, and manage team members with different positions. Features include task assignment,
priority management and deadline tracking.

## Installing / Getting started

A quick introduction of the minimal setup you need to get a hello world up &
running.

```bash
git clone https://github.com/alxitk/Task-Management.git
cd task-management-system/
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
After running these commands, navigate to http://127.0.0.1:8000/ to access the application.
```

You will need to log in with the superuser credentials you created since this is a portfolio project with authentication required.
user: task_admin
password: superuser

### Initial Configuration

git clone https://github.com/alxitk/Task-Management.git
cd task-management-system/
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
This will set up your development environment with all necessary dependencies and database migrations.


## Features

* Comprehensive Task Management: Create, update, delete, and track tasks with detailed information including deadlines, descriptions, and completion status
* Multi-user Task Assignment: Assign multiple workers to tasks and track individual progress
* Team & Position Management: Manage workers with custom positions and track team structure
* Priority System: Three-level priority system (Low, Medium, High) for task organization
* Advanced Filtering: Search and filter tasks by name, status, type, and assigned workers
* Task Type Classification: Categorize tasks by type with automatic task counting per type
* Kanban Workflow: Four-status task board (To Do, In Progress, Needs Review, Done)
* Position Analytics: Track worker counts per position with detailed breakdowns
* Worker Detail Views: Comprehensive worker profiles showing completed and pending tasks
* Dynamic Status Management: Change task status directly from task detail views
* Session Tracking: User visit tracking and session management
* Responsive Design: Clean, user-friendly interface with pagination
* Authentication System: Secure login with custom user model extending Django's AbstractUser

## Configuration

Task Configuration

#### Task Status Options:
To Do: `'Tasks ready to start'`  
In Progress: `'Currently active tasks'`  
Needs Review: `'Tasks awaiting review'`  
Done: `'Completed tasks'`

#### Task Priority Levels:
low: `'Low priority tasks'`  
medium: `'Medium priority (default)'`  
high: `'High priority tasks'`


## Links

Even though this information can be found inside the project on machine-readable
format like in a .json file, it's good to include a summary of most useful
links to humans using your project. You can include links like:

- Project homepage: https://task-management-09w3.onrender.com/
- Repository:  https://github.com/alxitk/Task-Management
- Issue tracker:  https://github.com/alxitk/Task-Management/issues
  - Note: This is a portfolio/educational project created for learning purposes.



