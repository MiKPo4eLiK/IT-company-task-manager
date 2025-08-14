from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from company.models import TaskType, Task, Position
from django.utils import timezone


class TaskCreateViewTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Bug")
        self.position = Position.objects.create(name="Dev")
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass", position=self.position
        )
        self.client.login(username="testuser", password="testpass")

    def test_create_task(self) -> None:
        response = self.client.post(reverse("company:task-create"), {
            "name": "Fix Error 500",
            "description": "Fix the error on homepage",
            "deadline": (timezone.now() + timezone.timedelta(days=5)).isoformat(),
            "is_completed": False,
            "priority": "High",
            "task_type": self.task_type.pk,
            "assignees": [self.user.pk],
        })

        self.assertEqual(response.status_code, 302)  # should redirect
        self.assertEqual(Task.objects.count(), 1)

        task = Task.objects.first()
        self.assertEqual(task.name, "Fix Error 500")
        self.assertIn(self.user, task.assignees.all())


class WorkerDetailViewTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Manager")
        self.worker = get_user_model().objects.create_user(
            username="john", password="1234", position=self.position
        )

    def test_worker_detail_view(self) -> None:
        url = reverse("company:worker-detail", kwargs={"pk": self.worker.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john")
        self.assertContains(response, self.worker.position.name)
