"""Django admin configuration for projects."""

from django.contrib import admin

from .models import Category, Project


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "color_hex", "team"]
    list_filter = ["team"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "team", "status", "budget_hours", "created_at"]
    list_filter = ["status", "team"]
    search_fields = ["name"]
