from django.db import IntegrityError
from django.utils import timezone


from django.test import TestCase

from tasks.models import Worker, Position, TaskType, Task


class WorkerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create()
        cls.worker = Worker.objects.create(
            username="username_1",
            first_name="first_name_1",
            last_name="last_name_1",
            position=cls.position,
        )

    def test_first_name_label(self):
        worker = Worker.objects.get(id=1)
        field_label = worker._meta.get_field("first_name").verbose_name
        self.assertEqual(field_label, "first name")

    def test_first_name_max_length(self):
        worker = Worker.objects.get(id=1)
        max_length = worker._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 150)

    def test_worker_str_method(self):
        worker = Worker.objects.get(id=1)
        expected_str = (
            f"{worker.first_name} "
            f"{worker.last_name} "
            f"({worker.position})"
        )
        self.assertEqual(str(worker), expected_str)

    def test_workers_ordering(self):
        Worker.objects.create(
            username="username_2",
        )
        Worker.objects.create(
            username="username_3",
        )
        workers_set = Worker.objects.all()
        usernames = [worker.username for worker in workers_set]
        self.assertEqual(usernames, sorted(usernames))


class PositionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(
            position="test position",
        )

    def test_position_str(self):
        expected_object_name = "test position"
        self.assertEqual(str(self.position), expected_object_name)

    def test_position_max_length(self):
        max_length = self.position._meta.get_field("position").max_length
        self.assertEqual(max_length, 100)


class TaskTypeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.task_type = TaskType.objects.create(
            name="test task type",
        )

    def test_task_type_str(self):
        expected_object_name = "test task type"
        self.assertEqual(str(self.task_type), expected_object_name)

    def test_name_max_length(self):
        max_length = self.task_type._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)


class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.task_type = TaskType.objects.create(name="test task type")
        cls.position = Position.objects.create(position="test position")
        cls.worker = Worker.objects.create(
            username="username_1",
            first_name="first_name_1",
            last_name="last_name_1",
            position=cls.position,
        )
        cls.task = Task.objects.create(
            name="test task",
            description="test task description",
            deadline=timezone.now(),
            is_completed=False,
            priority="low",
            task_type=cls.task_type,
            status="todo",
        )
        cls.task.assignees.add(cls.worker)

    def test_name_max_length(self):
        max_length = self.task._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)

    def test_task_str(self):
        expected_object_name = f"{self.task.name} ({self.task.status})"
        self.assertEqual(str(self.task), expected_object_name)

    def test_task_type_link(self):
        self.assertEqual(self.task.task_type.name, "test task type")

    def test_many_to_many_workers(self):
        worker_1 = Worker.objects.create(
            username="username_3",
            first_name="first_name_3",
            last_name="last_name_3",
        )
        worker_2 = Worker.objects.create(
            username="username_2",
            first_name="first_name_2",
            last_name="last_name_2",
        )
        self.task.assignees.add(worker_1, worker_2)

        self.assertIn(worker_1, self.task.assignees.all())
        self.assertIn(worker_2, self.task.assignees.all())
        self.assertEqual(self.task.assignees.count(), 3)

    def test_task_ordering(self):
        earlier_task = Task.objects.create(
            name="Earlier task",
            description="Something else",
            deadline=self.task.deadline - timezone.timedelta(days=1),
            is_completed=False,
            priority=Task.Priority.MEDIUM,
            task_type=self.task_type,
            status=Task.Status.TODO,
        )

        earlier_task.assignees.set([self.worker])

        tasks = Task.objects.all()
        self.assertEqual(tasks.first(), earlier_task)

    def test_priority_choices(self):
        field = self.task._meta.get_field("priority")
        choices = [choice[0] for choice in field.choices]
        self.assertIn(self.task.priority, choices)

    def test_status_choices(self):
        field = self.task._meta.get_field("status")
        choices = [choice[0] for choice in field.choices]
        self.assertIn(self.task.status, choices)

    def test_name_unique(self):
        with self.assertRaises(IntegrityError):
            Task.objects.create(
                name="test task",
                description="Duplicate",
                deadline=timezone.now(),
                task_type=self.task_type,
                status=Task.Status.TODO,
            )

    def test_default_values(self):
        self.assertFalse(self.task.is_completed)
        self.assertEqual(self.task.priority, Task.Priority.LOW)
        self.assertEqual(self.task.status, Task.Status.TODO)
