from django.urls import path

from tasks.views import index, TasksListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView, \
    WorkerListView, WorkerCreateView, WorkerUpdateView

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
    ]