from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from company.models import Task
from company.forms import TaskForm


class TaskCreationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
        self.url = reverse('company:task-create')
        self.template_name = 'company/task_create.html'

    def test_task_create_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertIsInstance(response.context['form'], TaskForm)
        self.assertContains(response, 'Create a new task')

    def test_task_create_post_valid_data(self):
        valid_data = {
            'title': 'Test Task',
            'description': 'This is a test task description.',
            'status': 'new',
        }

        initial_task_count = Task.objects.count()

        response = self.client.post(self.url, data=valid_data)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Task.objects.count(), initial_task_count + 1)

        new_task = Task.objects.first()
        self.assertEqual(new_task.title, 'Test Task')

    def test_task_create_post_invalid_data(self):
        invalid_data = {
            'description': 'This is a test task description with invalid data.',
        }

        initial_task_count = Task.objects.count()

        response = self.client.post(self.url, data=invalid_data)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Task.objects.count(), initial_task_count)

        self.assertTrue(response.context['form'].errors)

    def test_task_create_requires_login(self):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next={self.url}')
