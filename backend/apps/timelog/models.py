"""Time entry models for tracking work hours."""

import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class TimeEntry(models.Model):
    """A logged block of time against a project (and optionally a task)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="time_entries",
    )
    task = models.ForeignKey(
        "tasks.Task",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="time_entries",
    )
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="time_entries",
    )
    description = models.CharField(max_length=500, blank=True)
    date = models.DateField()
    hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01, message="Hours must be greater than zero."),
            MaxValueValidator(24, message="Hours cannot exceed 24 per entry."),
        ],
    )
    is_billable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "time entry"
        verbose_name_plural = "time entries"
        ordering = ["-date", "-created_at"]

    def __str__(self) -> str:
        return f"{self.user} — {self.hours}h on {self.date} ({self.project})"
