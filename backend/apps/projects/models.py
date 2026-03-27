"""Project and category models."""

import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """A colour-coded category for grouping projects within a team."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    color_hex = models.CharField(max_length=7, default="#01696f")
    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.CASCADE,
        related_name="categories",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class ProjectStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    ON_HOLD = "on_hold", "On Hold"
    COMPLETED = "completed", "Completed"
    ARCHIVED = "archived", "Archived"


class Project(models.Model):
    """A project groups tasks and tracks budget against a team."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.CASCADE,
        related_name="projects",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
    )
    status = models.CharField(
        max_length=20,
        choices=ProjectStatus.choices,
        default=ProjectStatus.ACTIVE,
    )
    budget_hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_projects",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "project"
        verbose_name_plural = "projects"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
