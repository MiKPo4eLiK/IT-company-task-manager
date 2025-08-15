from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TaskType, Position, Worker, Task, Tag


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "deadline", "priority", "is_completed", "task_type")
    list_filter = ("priority", "is_completed", "task_type", "tags")
    search_fields = ("name", "description")
    filter_horizontal = ("assignees", "tags")


@admin.register(Worker)
class CustomWorkerAdmin(UserAdmin):
    model = Worker
    list_display = ("username", "email", "first_name", "last_name", "position", "is_staff")
    list_filter = ("position", "is_staff", "is_superuser")
    fieldsets = UserAdmin.fieldsets + (
        ("Additional fields", {"fields": ("position",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional fields", {"fields": ("position",)}),
    )
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
