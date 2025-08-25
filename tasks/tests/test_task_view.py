from datetime import date

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from tasks.models import Worker, TaskType, Task


class TasksViewTest(TestCase):
    TASKS_URL = reverse("tasks:task-list")

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="test")
        cls.worker = Worker.objects.create(username="worker")
        cls.task_type = TaskType.objects.create(name="Simple")

        statuses = ["todo", "in_progress", "needs_review", "done"]
        for status in statuses:
            task = Task.objects.create(
                name=f"Task {status}",
                description="test",
                deadline=date.today(),
                task_type=cls.task_type,
                status=status,
            )
            task.assignees.set([cls.worker])

    def test_view_returns_200(self):
        self.client.force_login(self.user)
        response = self.client.get(self.TASKS_URL)
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.TASKS_URL)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_correct_template_used(self):
        self.client.force_login(self.user)
        response = self.client.get(self.TASKS_URL)
        self.assertTemplateUsed(response, "tasks/task_list.html")

    def test_context_contains_task_list(self):
        self.client.force_login(self.user)
        response = self.client.get(self.TASKS_URL)
        self.assertIn("todo_tasks", response.context)
        self.assertIn("in_progress_tasks", response.context)
        self.assertIn("needs_review_tasks", response.context)
        self.assertIn("done_tasks", response.context)

    def test_status_lists_only_contain_correct_status(self):
        task = Task.objects.create(
            name="Task 1",
            description="Task description",
            deadline=date.today(),
            task_type=TaskType.objects.create(name="Task Type"),
            status="todo",
        )
        self.client.force_login(self.user)
        response = self.client.get(self.TASKS_URL)
        self.assertIn(task, response.context["todo_tasks"])
        self.assertNotIn(task, response.context["in_progress_tasks"])
        self.assertNotIn(task, response.context["done_tasks"])
        self.assertNotIn(task, response.context["needs_review_tasks"])

    def test_view_filters_tasks_by_name(self):
        task1 = Task.objects.create(
            name="Fix bug",
            description="Bug in system",
            deadline=date.today(),
            status="todo",
            task_type=TaskType.objects.create(name="Type A"),
        )
        task2 = Task.objects.create(
            name="Add feature",
            description="New feature",
            deadline=date.today(),
            status="todo",
            task_type=TaskType.objects.create(name="Type B"),
        )
        self.client.force_login(self.user)
        response = self.client.get(self.TASKS_URL + "?name=fix")

        self.assertIn(task1, response.context["todo_tasks"])
        self.assertNotIn(task2, response.context["todo_tasks"])

    def test_view_contains_search_form(self):
        self.client.force_login(self.user)
        response = self.client.get(self.TASKS_URL)
        self.assertIn("search_form", response.context)
        self.assertEqual(response.context["search_form"].initial["name"], "")


class TaskCreateViewTest(TestCase):
    TASKS_URL = reverse("tasks:task-create")

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="test")
        cls.worker = Worker.objects.create(username="worker")
        cls.task_type = TaskType.objects.create(name="Simple")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.TASKS_URL)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_view_returns_200(self):
        self.client.force_login(self.user)
        response = self.client.get(self.TASKS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_form.html")

    def test_form_contains_expected_fields(self):
        self.client.force_login(self.user)
        response = self.client.get(self.TASKS_URL)
        form = response.context["form"]
        self.assertIn("description", form.fields)
        self.assertIn("name", form.fields)
        self.assertIn("deadline", form.fields)
        self.assertIn("status", form.fields)
        self.assertIn("task_type", form.fields)
        self.assertIn("assignees", form.fields)

    def test_form_contains_correct_fields(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.TASKS_URL,
            data={
                "name": "Task 1",
                "description": "Task description",
                "deadline": date.today(),
                "priority": "low",
                "task_type": self.task_type.id,
                "assignees": [self.worker.id],
                "status": "todo",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().name, "Task 1")
        self.assertEqual(Task.objects.first().assignees.count(), 1)

    def test_create_with_invalid_data(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.TASKS_URL,
            data={
                "name": "",
                "description": "Task description",
                "deadline": date.today(),
                "priority": "low",
                "task_type": self.task_type.id,
                "assignees": [self.worker.id],
                "status": "todo",
            },
        )
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertEqual(form.errors["name"], ["This field is required."])
        self.assertEqual(Task.objects.count(), 0)


class TaskUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="test")
        cls.worker = Worker.objects.create(username="worker")
        cls.task_type = TaskType.objects.create(name="Simple")
        cls.task = Task.objects.create(
            name="Task 1",
            description="Task description",
            deadline=date.today(),
            task_type=cls.task_type,
        )
        cls.task.assignees.add(cls.worker.id)
        cls.updated_url = reverse("tasks:task-update", args={cls.task.id})

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.updated_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_view_returns_200(self):
        self.client.force_login(self.user)
        response = self.client.get(self.updated_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_form.html")

    def test_valid_update(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.updated_url,
            data={
                "name": "Task 2",
                "description": "Task description",
                "deadline": date.today(),
                "task_type": self.task_type.id,
                "priority": "low",
                "status": "in_progress",
                "assignees": [self.worker.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Task 2")

    def test_invalid_update(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.updated_url,
            data={
                "name": "",
                "description": "Task description",
                "deadline": date.today(),
                "task_type": self.task_type.id,
                "priority": "low",
                "status": "in_progress",
                "assignees": [self.worker.id],
            },
        )
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertFalse(form.is_valid())

    def test_form_prefilled_with_existing_data(self):
        self.client.force_login(self.user)
        response = self.client.get(self.updated_url)
        form = response.context["form"]
        self.assertEqual(form.initial["name"], "Task 1")
        self.assertEqual(list(form.initial["assignees"]), [self.worker])


class TaskDeleteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="test")
        cls.worker = Worker.objects.create(username="worker")
        cls.task_type = TaskType.objects.create(name="Simple")
        cls.task = Task.objects.create(
            name="Task 1",
            description="Task description",
            deadline=date.today(),
            task_type=cls.task_type,
            priority="low",
            status="in_progress",
        )
        cls.task.assignees.add(cls.worker)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse("tasks:task-delete", args=[self.task.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_view_returns_200(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("tasks:task-delete", args=[self.task.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_successful_delete_redirects_and_removes_object(self):
        self.client.force_login(self.user)
        url = reverse("tasks:task-delete", args=[self.task.id])
        self.client.get(url)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)
        self.assertRedirects(response, reverse("tasks:task-list"))

    def test_delete_nonexistent_task_returns_404(self):
        self.client.force_login(self.user)
        url = reverse("tasks:task-delete", args=[99])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TaskDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="test")
        cls.worker = Worker.objects.create(username="worker")
        cls.task_type = TaskType.objects.create(name="Simple")
        cls.task = Task.objects.create(
            name="Task 1",
            description="Task description",
            deadline=date.today(),
            task_type=cls.task_type,
            priority="low",
            status="in_progress",
        )
        cls.task.assignees.add(cls.worker)
        cls.task_url = reverse("tasks:task-detail", args=[cls.task.id])

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.task_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_detail.html")
        self.assertContains(response, "Task 1")

    def test_404_if_task_not_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks:task-detail", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_context_contains_correct_task(self):
        self.client.force_login(self.user)
        response = self.client.get(self.task_url)
        self.assertEqual(response.context["task"], self.task)
