"""Django admin configuration for timelog."""

from django.contrib import admin

from .models import TimeEntry


@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ["user", "project", "task", "date", "hours", "is_billable"]
    list_filter = ["date", "is_billable", "project"]
    search_fields = ["description"]
