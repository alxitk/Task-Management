from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from tasks.forms import TaskSearchForm
from tasks.models import Worker, Task, TaskType, Position


@login_required
def index(request):
    """View function for the home page of the site."""

    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()
    num_task_types = TaskType.objects.count()
    num_positions = Position.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "num_task_types": num_task_types,
        "num_positions": num_positions,
        "num_visits": num_visits + 1,
    }

    return render(request, "tasks/index.html", context=context)


class TasksListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "tasks/task_list.html"
    queryset = Task.objects.all()

    def get_queryset(self):
        name = self.request.GET.get("name", "")
        task_type_id = self.kwargs.get("task_type_id")
        queryset = super().get_queryset()
        if task_type_id:
            queryset = queryset.filter(task_type_id=task_type_id)
        if name:
            return queryset.filter(name__icontains=name)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        filtered_queryset = self.get_queryset()

        context["todo_tasks"] = filtered_queryset.filter(status="todo")
        context["in_progress_tasks"] = filtered_queryset.filter(
            status="in_progress"
        )
        context["done_tasks"] = filtered_queryset.filter(status="done")
        context["needs_review_tasks"] = filtered_queryset.filter(
            status="needs_review"
        )

        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(initial={"name": name})
        return context


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task