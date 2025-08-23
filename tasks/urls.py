from django.urls import path

from tasks.views import index, TasksListView, TaskDetailView, TaskCreateView

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
    ]