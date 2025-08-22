from django import forms


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