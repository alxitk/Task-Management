from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tasks.models import Task, TaskType, Position, Worker

admin.site.register(TaskType)
admin.site.register(Position)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name", "deadline", "priority", "is_completed", "task_type"
    )
    search_fields = ("name",)
    list_filter = ("is_completed", "task_type", "deadline")


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    ordering = ("last_name",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "position",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "position")
    search_fields = (
        "username",
        "first_name",
        "last_name",
    )
    fieldsets = UserAdmin.fieldsets + (
        (("Position", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                    )
                },
            ),
        )
    )
