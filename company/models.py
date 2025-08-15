from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import CharField
from django.urls import reverse


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name}"


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name}"


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self) -> str:
        return reverse("company:worker-detail", kwargs={"pk": self.pk})


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> CharField:
        return self.name


class Task(models.Model):
    class PriorityChoices(models.TextChoices):
        URGENT = "Urgent", "Urgent"
        HIGH = "High", "High"
        MEDIUM = "Medium", "Medium"
        LOW = "Low", "Low"

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=50,
        choices=PriorityChoices.choices,
        default=PriorityChoices.MEDIUM,
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.PROTECT)
    assignees = models.ManyToManyField(Worker, related_name="tasks")
    tags = models.ManyToManyField(Tag, related_name="tasks", blank=True)

    class Meta:
        verbose_name = "task"
        verbose_name_plural = "tasks"
        ordering = ["is_completed", "priority", "deadline"]

    def __str__(self) -> str:
        return f"{self.name} ({self.task_type})"

    def get_absolute_url(self) -> str:
        return reverse("company:task-detail", kwargs={"pk": self.pk})
