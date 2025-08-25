from django.urls import path

from tasks.views import index, TasksListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView, \
    WorkerListView, WorkerCreateView, WorkerUpdateView, WorkerDeleteView, WorkerDetailView, toggle_assign_to_task, \
    PositionListView, PositionCreateView, PositionUpdateView, PositionDeleteView, TaskTypesListView, TaskTypeCreateView, \
    TaskTypeUpdateView, TaskTypeDeleteView, CustomLoginView, set_task_status, manage_task_users, TaskStatusListView

app_name = "tasks"

urlpatterns = [
    path("", index, name="index"),
    path(
        "tasks/",
        TasksListView.as_view(),
        name="task-list",
    ),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path(
        "tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"
    ),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("worker/create/", WorkerCreateView.as_view(), name="worker-create"),
    path(
        "worker/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update"
    ),
    path(
        "worker/<int:pk>/delete/",
        WorkerDeleteView.as_view(),
        name="worker-delete"
    ),
    path("worker/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path(
        "tasks/<int:pk>/toggle-assign/",
        toggle_assign_to_task,
        name="toggle-task-assign",
    ),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path(
        "positions/create/",
        PositionCreateView.as_view(),
        name="position-create",
    ),
    path(
        "positions/<int:pk>/update/",
        PositionUpdateView.as_view(),
        name="position-update",
    ),
    path(
        "positions/<int:pk>/delete/",
        PositionDeleteView.as_view(),
        name="position-delete",
    ),
    path(
        "task_types/",
        TaskTypesListView.as_view(),
        name="task_types_list",
    ),
    path(
        "task_types/create/",
        TaskTypeCreateView.as_view(),
        name="task_type_create",
    ),
    path(
        "task_types/<int:pk>/update/",
        TaskTypeUpdateView.as_view(),
        name="task_type_update",
    ),
    path(
        "task_types/<int:pk>/delete/",
        TaskTypeDeleteView.as_view(),
        name="task_type_delete",
    ),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path("task/<int:pk>/set-status/", set_task_status, name="set-status"),
    path(
        "tasks/<int:pk>/manage-users/",
        manage_task_users,
        name="manage-task-users"
    ),
    path("tasks/status/<str:status>/", TaskStatusListView.as_view(), name="task-status-list"),
    path(
        "task_types/<int:task_type_id>/tasks/",
        TasksListView.as_view(),
        name="task-type-tasks",
    ),
    ]