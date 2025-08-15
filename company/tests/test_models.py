from django.test import TestCase
from company.models import TaskType, Task, Worker, Position
from django.utils import timezone
from django.contrib.auth import get_user_model

class TaskModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = get_user_model().objects.create_user(
            username="worker1", password="pass", position=self.position
        )
        self.task_type = TaskType.objects.create(name="Bugfix")

    def test_task_creation(self):
        task = Task.objects.create(
            name="Fix login bug",
            description="Fix issue with user login",
            deadline=timezone.now() + timezone.timedelta(days=3),
            is_completed=False,
            priority="High",
            task_type=self.task_type
        )
        task.assignees.add(self.worker)

        self.assertEqual(task.name, "Fix login bug")
        self.assertIn(self.worker, task.assignees.all())
