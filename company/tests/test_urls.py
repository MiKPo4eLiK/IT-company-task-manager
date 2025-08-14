from django.test import SimpleTestCase
from django.urls import reverse, resolve
from company.views import FilteredTaskListView

class TestUrls(SimpleTestCase):
    def test_task_list_url(self):
        url = reverse("company:filtered-task-list")
        self.assertEqual(resolve(url).func.view_class, FilteredTaskListView)
