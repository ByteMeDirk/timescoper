"""Django admin configuration for tasks."""

from django.contrib import admin

from .models import Task, TaskComment, TaskLabel


@admin.register(TaskLabel)
class TaskLabelAdmin(admin.ModelAdmin):
    list_display = ["name", "color_hex", "team"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "project", "assigned_to", "status", "priority", "due_date"]
    list_filter = ["status", "priority", "project"]
    search_fields = ["title"]


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ["task", "author", "created_at"]
