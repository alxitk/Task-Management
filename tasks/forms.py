from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from tasks.models import Task, Worker, Position, TaskType


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


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search worker by username...",
                "class": "search-input",
            }
        ),
    )


class WorkerCreateForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "input white-background", "placeholder": "Password"}
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"class": "input white-background",
                   "placeholder": "Confirm Password"}
        ),
        strip=False,
    )

    class Meta:
        model = Worker
        fields = (
            "username",
            "first_name",
            "last_name",
            "position",
            "password1",
            "password2",
        )
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "input white-background", "placeholder": "Username"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "input white-background",
                       "placeholder": "First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "input white-background",
                       "placeholder": "Last Name"}
            ),
            "position": forms.Select(attrs={"class": "input white-background"}),
        }


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ("username", "first_name", "last_name", "position")
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "input white-background", "placeholder": "Username"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "input white-background",
                       "placeholder": "First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "input white-background",
                       "placeholder": "Last Name"}
            ),
            "position": forms.Select(attrs={"class": "input white-background"}),
        }


class PositionSearchForm(forms.Form):
    position = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search position...",
                "class": "search-input",
            }
        ),
    )


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = "__all__"
        widgets = {
            "position": forms.TextInput(attrs={"class": "input white-background",
                                               "placeholder": "Enter position..."}),
        }


class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "input white-background",
                                           "placeholder": "Enter task type name..."}),
        }


class TaskTypeSearchForm(forms.Form):
    name = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search task type...",
                "class": "search-input",
            }
        ),
    )


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input',})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input',})
    )


class AssignUserForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="",
    )