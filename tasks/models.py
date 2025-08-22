from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Position(models.Model):
    position = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.position


class Worker(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"
        ordering = ("username",)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"


class TaskType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Task(models.Model):

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    class Status(models.TextChoices):
        TODO = "todo", "To Do"
        IN_PROGRESS = "in_progress", "In Progress"
        NEEDS_REVIEW = "needs_review", "Needs Review"
        DONE = "done", "Done"

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.MEDIUM
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker, related_name="tasks")
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.TODO
    )

    class Meta:
        ordering = ("deadline",)

    def __str__(self):
        return f"{self.name} ({self.status})"
