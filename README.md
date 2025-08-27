Task Management System
Django-based team task management application

A comprehensive task management system built with Django that enables teams to organize work efficiently, track task progress, and manage team members with different positions. Features include task assignment, priority management and deadline tracking.

Installing / Getting started
A quick setup to get the project running locally:

bash
git clone https://github.com/alxitk/Task-Management.git
cd task-management-system/
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
After running these commands, navigate to http://127.0.0.1:8000/ to access the application. You'll need to log in with the superuser credentials you created since this is a portfolio project with authentication required.

Initial Configuration

bash
git clone https://github.com/alxitk/Task-Management.git
cd task-management-system/
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
This will set up your development environment with all necessary dependencies and database migrations.


Features
This task management system provides:

Comprehensive Task Management: Create, update, delete, and track tasks with detailed information including deadlines, descriptions, and completion status
Priority System: Three-level priority system (Low, Medium, High) for task organization
Team & Position Management: Manage workers with custom positions and track team structure
Multi-user Task Assignment: Assign multiple workers to tasks and track individual progress
Kanban Workflow: Four-status task board (To Do, In Progress, Needs Review, Done)
Task Type Classification: Categorize tasks by type with automatic task counting per type
Advanced Filtering: Search and filter tasks by name, status, type, and assigned workers
Position Analytics: Track worker counts per position with detailed breakdowns
Worker Detail Views: Comprehensive worker profiles showing completed and pending tasks
Dynamic Status Management: Change task status directly from task detail views
Session Tracking: User visit tracking and session management
Responsive Design: Clean, user-friendly interface with pagination
Authentication System: Secure login with custom user model extending Django's AbstractUser
Configuration
Task Configuration
Task Status Options:

todo: To Do - Tasks ready to start
in_progress: In Progress - Currently active tasks
needs_review: Needs Review - Tasks awaiting review
done: Done - Completed tasks
Task Priority Levels:

low: Low priority tasks
medium: Medium priority (default)
high: High priority tasks
Task Fields:

Name (unique, max 100 characters)
Description (optional, text field)
Deadline (required datetime)
Completion status (boolean)
Priority level (required)
Task type (required, foreign key)
Multiple assignees (many-to-many relationship)
Worker Configuration
Workers are custom users with additional fields:

First name (required)
Last name (required)
Position (optional, foreign key to Position model)
All standard Django User fields (username, email, etc.)
Pagination
Default: 5 items per page for all list views Modify the paginate_by attribute in ListView classes to change this setting.

Application Structure
Core Models
Task: Main task entity with name, description, deadline, priority, type, assignees, and status
Worker: Custom user model extending AbstractUser with position information
Position: Job positions/roles within the organization
TaskType: Categories for organizing different types of tasks
Key Views & URLs
/ - Dashboard with system statistics (tasks, workers, positions, task types)
/tasks/ - Kanban-style task board with status columns
/tasks/status/<status>/ - Tasks filtered by specific status
/tasks/<id>/ - Detailed task view with assignment management
/workers/ - Worker list with search and position filtering
/workers/<id>/ - Worker detail view showing assigned tasks
/positions/ - Position management with worker count annotations
/task-types/ - Task type management with task count statistics
Dependencies
Django==5.2.5
django-crispy-forms==2.4
django-extensions==4.1
python-dotenv==1.1.1
black==25.1.0 (development)
flake8==7.3.0 (development)

Links

Repository: https://github.com/alxitk/Task-Management
Issue tracker: https://github.com/alxitk/Task-Management/issues
Related technologies:
Django Documentation: https://docs.djangoproject.com/
Django Crispy Forms: https://django-crispy-forms.readthedocs.io/
Python dotenv: https://pypi.org/project/python-dotenv/
Note: This is a portfolio/educational project created for learning purposes.
