from django import forms
from django.contrib.auth import get_user_model

from tasks.models import Task


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by task name...",
                "class": "search-input",
            }
        ),
    )


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "checkbox-list"}
        ),
        label="Assignees",
        required=False,
    )

    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "input white-background",
            }
        ),
        label="Deadline",
    )

    class Meta:
        model = Task
        fields = (
            "name",
            "description",
            "deadline",
            "priority",
            "task_type",
            "assignees",
            "status",
        )
        labels = {
            "name": "Task Name",
            "description": "Description",
            "deadline": "Deadline",
            "priority": "Priority",
            "task_type": "Task Type",
            "assignees": "Assignees",
            "status": "Task Status",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "input white-background", "placeholder": "Enter task name..."}
            ),
            "description": forms.Textarea(
                attrs={"class": "input white-background description", "rows": 40, "placeholder": "Enter task description..."}
            ),
            "priority": forms.Select(
                attrs={"class": "input white-background"}
            ),
            "task_type": forms.Select(
                attrs={"class": "input white-background"}
            ),
            "status": forms.Select(
                attrs={"class": "input white-background"}
            ),
        }