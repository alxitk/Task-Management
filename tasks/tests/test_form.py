from django.test import TestCase


from tasks.forms import (
    WorkerCreateForm,
    WorkerSearchForm,
    TaskSearchForm,
    WorkerUpdateForm,
    TaskForm,
    AssignUserForm,
)
from tasks.models import Position, Worker, Task, TaskType
from django.forms.widgets import CheckboxSelectMultiple


class WorkerCreationFormTests(TestCase):

    def test_worker_form(self):
        position = Position.objects.create(position="designer")
        form_data = {
            "username": "testworker",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
            "position": position,
            "first_name": "John",
            "last_name": "Doe",
        }
        form = WorkerCreateForm(form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testworker")
        self.assertEqual(form.cleaned_data["first_name"], "John")
        self.assertEqual(form.cleaned_data["last_name"], "Doe")
        self.assertEqual(form.cleaned_data["position"], position)
        worker = form.save()
        self.assertEqual(worker.username, "testworker")
        self.assertEqual(worker.position, position)


class WorkerSearchFormTest(TestCase):
    def test_form_has_username_field(self):
        form = WorkerSearchForm()
        self.assertIn("username", form.fields)

    def test_form_valid_with_username(self):
        form = WorkerSearchForm(data={"username": "testworker"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testworker")

    def test_form_valid_with_empty_data(self):
        form = WorkerSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")


class WorkerUpdateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(position="testposition")
        cls.worker = Worker.objects.create(
            username="testworker",
            first_name="John",
            last_name="Doe",
            position=cls.position,
        )

    def test_form_valid_with_updated_username(self):
        form_data = {
            "username": "testworker_2",
            "first_name": "John",
            "last_name": "Doe",
            "position": self.worker.position,
        }
        form = WorkerUpdateForm(data=form_data, instance=self.worker)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testworker_2")
        form.save()
        self.worker.refresh_from_db()
        self.assertEqual(self.worker.username, "testworker_2")


class TaskSearchFormTest(TestCase):
    def test_form_has_name_field(self):
        form = TaskSearchForm()
        self.assertIn("name", form.fields)

    def test_form_valid_with_name(self):
        form = TaskSearchForm(data={"name": "testname"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "testname")

    def test_form_valid_with_empty_data(self):
        form = TaskSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")


class TaskFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.task_type = TaskType.objects.create(name="testtasktype")
        cls.position = Position.objects.create(
            position="testposition",
        )
        cls.worker = Worker.objects.create(
            username="testworker",
            first_name="John",
            last_name="Doe",
            position=cls.position,
        )
        cls.form_data = {
            "name": "testtask",
            "description": "testdescription",
            "deadline": "2025-12-31T12:00",
            "is_completed": False,
            "priority": Task.Priority.LOW,
            "task_type": cls.task_type.id,
            "assignees": [cls.worker.id],
            "status": Task.Status.IN_PROGRESS,
        }

    def test_form_valid_with_valid_assignees(self):
        form = TaskForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertIn(self.worker, form.cleaned_data["assignees"])

    def test_assignees_widget(self):
        form = TaskForm()
        field = form.fields["assignees"]
        self.assertIsInstance(field.widget, CheckboxSelectMultiple)


class AssignUserFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(position="testposition")
        cls.worker = Worker.objects.create(
            username="testworker",
            first_name="John",
            last_name="Doe",
            position=cls.position,
        )
        cls.worker_2 = Worker.objects.create(
            username="testworker_2",
            first_name="John_2",
            last_name="Doe_2",
            position=cls.position,
        )

    def test_form_valid_with_existing_user(self):
        form = AssignUserForm(data={"users": [self.worker.id]})
        self.assertTrue(form.is_valid())
        self.assertIn(self.worker, form.cleaned_data["users"])

    def test_users_field_has_checkbox_widget(self):
        form = AssignUserForm()
        field = form.fields["users"]
        self.assertIsInstance(field.widget, CheckboxSelectMultiple)
