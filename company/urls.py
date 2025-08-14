from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "company"

urlpatterns = [
    # Auth URLs
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Index
    path("", views.index, name="index"),

    # Worker URLs
    path("workers/", views.WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", views.WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/create/", views.WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/update/", views.WorkerLicenseUpdateView.as_view(), name="worker-update"),
    path("workers/<int:pk>/delete/", views.WorkerDeleteView.as_view(), name="worker-delete"),

    # TaskType URLs
    path("task-types/", views.TaskTypeListView.as_view(), name="task-type-list"),
    path("task-types/create/", views.TaskTypeCreateView.as_view(), name="task-type-create"),
    path("task-types/<int:pk>/update/", views.TaskTypeUpdateView.as_view(), name="task-type-update"),
    path("task-types/<int:pk>/delete/", views.TaskTypeDeleteView.as_view(), name="task-type-delete"),

    # Position URLs
    path("positions/", views.PositionListView.as_view(), name="position-list"),
    path("positions/create/", views.PositionCreateView.as_view(), name="position-create"),
    path("positions/<int:pk>/update/", views.PositionUpdateView.as_view(), name="position-update"),
    path("positions/<int:pk>/delete/", views.PositionDeleteView.as_view(), name="position-delete"),

    # Tag URLs
    path("tags/", views.TagListView.as_view(), name="tag-list"),
    path("tags/create/", views.TagCreateView.as_view(), name="tag-create"),
    path("tags/<int:pk>/update/", views.TagUpdateView.as_view(), name="tag-update"),
    path("tags/<int:pk>/delete/", views.TagDeleteView.as_view(), name="tag-delete"),

    # Task URLs
    path("tasks/", views.TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", views.TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", views.TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/toggle-assign/", views.toggle_assign_to_worker, name="toggle-assign-to-worker"),
]
