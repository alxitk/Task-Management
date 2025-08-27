from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from tasks.models import Task, TaskType, Worker


class TestIndex(TestCase):
    INDEX_URL = reverse("tasks:index")

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_success_url(self):
        self.client.force_login(self.user)
        response = self.client.get(self.INDEX_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/index.html")

    def test_index_view_displays_correct_number_of_tasks(self):
        self.client.force_login(self.user)
        worker = Worker.objects.create(
            username="test username",
        )

        task = Task.objects.create(
            name="Task 1",
            description="Task description",
            deadline=date.today(),
            task_type=TaskType.objects.create(name="Task Type"),
        )
        task.assignees.set([worker])
        response = self.client.get(self.INDEX_URL)
        self.assertIn("num_tasks", response.context)
        self.assertEqual(response.context["num_tasks"], 1)

    def test_index_shows_worker_count(self):
        self.client.force_login(self.user)
        for i in range(10):
            Worker.objects.create(
                username="test username" + str(i),
            )
        response = self.client.get(self.INDEX_URL)
        self.assertEqual(response.context["num_workers"], 11)

    def test_index_initial_session_visit_count_is_one(self):
        self.client.force_login(self.user)
        response = self.client.get(self.INDEX_URL)
        self.assertEqual(response.context["num_visits"], 1)
        self.assertEqual(self.client.session["num_visits"], 1)

    def test_index_session_visit_counter_increments_on_each_visit(self):
        self.client.force_login(self.user)
        response = self.client.get(self.INDEX_URL)
        self.assertEqual(response.context["num_visits"], 1)
        response = self.client.get(self.INDEX_URL)
        self.assertEqual(response.context["num_visits"], 2)
        self.assertEqual(self.client.session["num_visits"], 2)
