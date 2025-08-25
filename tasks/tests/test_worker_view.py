from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from tasks.models import Position, Worker, Task, TaskType


class WorkerListViewTest(TestCase):
    WORKER_URL = reverse("tasks:worker-list")

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="test")
        cls.position = Position.objects.create(position="Test position")
        cls.workers = [
            Worker.objects.create_user(
                username=f"user{i}",
                first_name="First",
                last_name="Last",
                position=cls.position,
                password="testpassword123",
            )
            for i in range(7)
        ]
        cls.worker = cls.workers[0]

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.WORKER_URL)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_worker_list_view_returns_200_and_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.WORKER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/worker_list.html")

    def test_worker_list_view_contains_all_workers(self):
        self.client.force_login(self.user)
        response = self.client.get(self.WORKER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.worker, response.context["worker_list"])
        self.assertEqual(len(response.context["worker_list"]), 5)

    def test_worker_list_view_displays_worker_details(self):
        self.client.force_login(self.user)
        response = self.client.get(self.WORKER_URL)
        self.assertContains(response, self.worker.username)
        self.assertContains(response, self.worker.first_name)
        self.assertContains(response, self.worker.last_name)
        self.assertContains(response, self.worker.position.position)

    def test_search_form_in_context(self):
        self.client.force_login(self.user)
        response = self.client.get(self.WORKER_URL + "?username=worker")
        self.assertIn("search_form", response.context)
        self.assertEqual(
            response.context["search_form"].initial["username"], "worker"
        )

    def test_worker_queryset_filtered_by_first_name(self):
        self.client.force_login(self.user)
        worker_Alex = Worker.objects.create(
            username="Alex",
            first_name="Test first name",
            last_name="Test last name",
            position=self.position,
        )

        response = self.client.get(self.WORKER_URL + "?username=Alex")

        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertEqual(
            response.context["search_form"].initial["username"], "Alex"
        )

        workers = response.context["worker_list"]
        self.assertEqual(len(workers), 1)
        self.assertEqual(workers[0].username, "Alex")

    def test_worker_list_view_returns_empty_when_no_match(self):
        self.client.force_login(self.user)
        response = self.client.get(self.WORKER_URL + "?username=Alex")
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertEqual(
            response.context["search_form"].initial["username"], "Alex"
        )

        workers = response.context["worker_list"]
        self.assertEqual(len(workers), 0)

    def test_pagination_is_five(self):
        self.client.force_login(self.user)
        response = self.client.get(self.WORKER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["worker_list"]), 5)

    def test_lists_all_workers(self):
        self.client.force_login(self.user)
        response = self.client.get(self.WORKER_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["worker_list"]), 3)


class WorkerDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="test")
        cls.position = Position.objects.create(position="Test position")
        cls.worker = Worker.objects.create(
            username="Test worker",
            first_name="Test first name",
            last_name="Test last name",
            position=cls.position,
        )
        cls.worker_url = reverse("tasks:worker-detail", args=[cls.worker.id])

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.worker_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.worker_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/worker_detail.html")
        self.assertContains(response, "Test worker")

    def test_404_if_worker_not_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks:worker-detail", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_displays_worker_details(self):
        self.client.force_login(self.user)
        response = self.client.get(self.worker_url)
        self.assertContains(response, str(self.worker.id))
        self.assertContains(response, self.worker.username)
        self.assertContains(response, self.worker.first_name)
        self.assertContains(response, self.worker.last_name)
        self.assertContains(response, self.worker.position.position)

    def test_detail_view_context_contains_worker(self):
        self.client.force_login(self.user)
        response = self.client.get(self.worker_url)
        self.assertEqual(response.context["worker"], self.worker)

    def test_detail_view_displays_worker_tasks_grouped_by_status(self):
        self.client.force_login(self.user)
        worker = Task.objects.create(
            name="Test task",
            description="Test description",
            deadline=timezone.now(),
            is_completed=False,
            priority=Task.Priority.LOW,
            task_type=TaskType.objects.create(name="Test task type"),
            status=Task.Status.IN_PROGRESS,
        )
        worker.assignees.add(self.worker)

        response = self.client.get(self.worker_url)
        self.assertIn(worker, response.context["worker"].tasks.all())
        self.assertContains(response, "Incomplete Tasks")

    def test_view_displays_no_tasks_message_when_worker_has_no_tasks(self):
        self.client.force_login(self.user)
        response = self.client.get(self.worker_url)
        self.assertEqual(self.worker.tasks.count(), 0)
        self.assertEqual(response.context["worker"], self.worker)
        self.assertContains(response, "No completed tasks.")


class WorkerDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="test")
        cls.position = Position.objects.create(position="Test position")
        cls.worker = Worker.objects.create(
            username="Test worker",
            first_name="Test first name",
            last_name="Test last name",
            position=cls.position,
        )
        cls.worker_url = reverse(
            "tasks:worker-delete", kwargs={"pk": cls.worker.id}
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.worker_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_delete_worker_success(self):
        self.client.force_login(self.user)
        response = self.client.post(self.worker_url)
        self.assertRedirects(response, reverse("tasks:worker-list"))
        self.assertFalse(Worker.objects.filter(id=self.worker.id).exists())

    def test_template_used(self):
        self.client.force_login(self.user)
        response = self.client.get(self.worker_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/worker_confirm_delete.html")


class WorkerCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="test")
        cls.position = Position.objects.create(position="Test position")

    def test_create_worker_success(self):
        self.client.force_login(self.user)
        form_data = {
            "username": "newworker",
            "first_name": "John",
            "last_name": "Doe",
            "position": self.position.id,
            "password1": "testpass123",
            "password2": "testpass123",
        }
        response = self.client.post(
            reverse("tasks:worker-create"), data=form_data
        )
        self.assertRedirects(response, reverse("tasks:worker-list"))
        self.assertTrue(Worker.objects.filter(username="newworker").exists())

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("tasks:worker-list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_create_worker_template_used(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks:worker-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/worker_form.html")


class WorkerUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="test")
        cls.position = Position.objects.create(position="Test position")
        cls.worker = Worker.objects.create_user(
            username="oldworker",
            first_name="Old",
            last_name="Name",
            position=cls.position,
            password="testpass123",
        )
        cls.update_url = reverse(
            "tasks:worker-update", kwargs={"pk": cls.worker.id}
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_update_worker_success(self):
        self.client.force_login(self.user)
        form_data = {
            "username": "updatedworker",
            "first_name": "NewFirst",
            "last_name": "NewLast",
            "position": self.position.id,
        }
        response = self.client.post(self.update_url, data=form_data)
        self.assertRedirects(response, reverse("tasks:worker-list"))
        self.worker.refresh_from_db()
        self.assertEqual(self.worker.username, "updatedworker")
        self.assertEqual(self.worker.first_name, "NewFirst")
        self.assertEqual(self.worker.last_name, "NewLast")

    def test_update_worker_template_used(self):
        self.client.force_login(self.user)
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/worker_form.html")

    def test_update_worker_invalid_data(self):
        self.client.force_login(self.user)
        form_data = {
            "username": "",
            "first_name": "Test",
            "last_name": "User",
            "position": self.position.id,
        }
        response = self.client.post(self.update_url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"], "username", "This field is required."
        )
        self.worker.refresh_from_db()
        self.assertEqual(self.worker.username, "oldworker")


class WorkerSearchFormTest(TestCase):
    WORKER_URL = reverse("tasks:worker-list")

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", password="testpass123"
        )
        cls.position = Position.objects.create(position="Test position 123")
        number_of_workers = 13
        for i in range(number_of_workers):
            Worker.objects.create_user(
                username=f"test worker{i}",
                password="testpass123",
                position=cls.position,
                first_name=f"First{i}",
                last_name=f"Last{i}",
            )

    def test_search_form_in_context(self):
        self.client.force_login(self.user)
        response = self.client.get(self.WORKER_URL + "?username=test worker")
        self.assertIn("search_form", response.context)
        self.assertEqual(
            response.context["search_form"].initial["username"], "test worker"
        )

    def test_worker_queryset_filtered_by_username(self):
        self.client.force_login(self.user)
        position = Position.objects.create(position="Test position")
        Worker.objects.create_user(
            username="bobdy",
            password="testpass123",
            position=position,
            first_name="Bob",
            last_name="Dylan",
        )
        Worker.objects.create_user(
            username="test worker 1",
            password="testpass123",
            position=position,
            first_name="First",
            last_name="Last",
        )

        response = self.client.get(self.WORKER_URL + "?username=Bob")

        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertEqual(
            response.context["search_form"].initial["username"], "Bob"
        )

        workers = response.context["worker_list"]
        self.assertEqual(len(workers), 1)
        self.assertEqual(workers[0].first_name, "Bob")
