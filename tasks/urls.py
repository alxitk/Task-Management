from django.urls import path

from tasks.views import index, TasksListView

app_name = "tasks"

urlpatterns = [
    path("", index, name="index"),
    path(
        "tasks/",
        TasksListView.as_view(),
        name="task-list",
    ),
    ]