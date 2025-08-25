from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views import generic

from tasks.forms import TaskSearchForm, TaskForm, WorkerSearchForm, WorkerCreateForm, WorkerUpdateForm, \
    PositionSearchForm, PositionForm, TaskTypeForm, TaskTypeSearchForm, CustomAuthenticationForm, AssignUserForm
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


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

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


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")


class TaskStatusListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "tasks/task_status_list.html"
    paginate_by = 5

    STATUS_TITLES = {
        "todo": "To Do",
        "in_progress": "In Progress",
        "needs_review": "Needs Review",
        "done": "Done",
    }

    def get_queryset(self):
        status = self.kwargs.get("status")
        return Task.objects.filter(status=status)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        status = self.kwargs.get("status")
        context["now"] = now()
        context["task_status"] = self.STATUS_TITLES.get(status, "Tasks")
        return context


def set_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    new_status = request.POST.get("status")

    if new_status in Task.Status.values:
        task.status = new_status
        task.save()

    return redirect("tasks:task-detail", pk=task.pk)


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    context_object_name = "worker_list"
    template_name = "tasks/worker_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = Worker.objects.select_related("position")
        username = self.request.GET.get("username", "")

        if username:
            return queryset.filter(username__icontains=username)

        position_id = self.kwargs.get("position_id")
        if position_id:
            return queryset.filter(position__id=position_id)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(
            initial={"username": username}
        )
        return context


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreateForm
    success_url = reverse_lazy("tasks:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("tasks:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("tasks:worker-list")


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    queryset = Worker.objects.all().prefetch_related("tasks__assignees")


def toggle_assign_to_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    user = request.user
    if user in task.assignees.all():
        task.assignees.remove(user)
    else:
        task.assignees.add(user)
    return HttpResponseRedirect(reverse_lazy("tasks:task-detail", args=[pk]))


def manage_task_users(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        form = AssignUserForm(request.POST)
        if form.is_valid():
            selected_users = form.cleaned_data["users"]

            task.assignees.set(selected_users)
            return redirect("tasks:task-detail", pk=pk)
    else:
        form = AssignUserForm(initial={"users": task.assignees.all()})

    return render(
        request, "tasks/manage_users_for_task.html", {"task": task, "form": form}
    )


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    context_object_name = "position_list"
    template_name = "tasks/position_list.html"
    paginate_by = 5
    queryset = Position.objects.all()

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        position = self.request.GET.get("position", "")
        context["search_form"] = PositionSearchForm(
            initial={"position": position}
        )
        return context

    def get_queryset(self):
        position = self.request.GET.get("position", "")
        queryset = Position.objects.annotate(worker_count=Count("worker"))
        if position:
            queryset = queryset.filter(position__icontains=position)
        return queryset


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("tasks:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("tasks:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("tasks:position-list")


class TaskTypesListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    context_object_name = "task_type_list"
    template_name = "tasks/tasktype_list.html"
    paginate_by = 5
    queryset = TaskType.objects.all()

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super(TaskTypesListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        name = self.request.GET.get("name", "")
        queryset = TaskType.objects.annotate(tasks_count=Count("task"))
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    form_class = TaskTypeForm
    success_url = reverse_lazy("tasks:task_types_list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    form_class = TaskTypeForm
    success_url = reverse_lazy("tasks:task_types_list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("tasks:task_types_list")