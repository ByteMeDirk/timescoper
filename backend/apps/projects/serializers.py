"""Serializers for the projects app."""

from django.db.models import Sum
from rest_framework import serializers

from .models import Category, Project


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "color_hex", "team", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class ProjectSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True, default=None)
    created_by_name = serializers.CharField(source="created_by.full_name", read_only=True)
    total_logged_hours = serializers.SerializerMethodField()
    task_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "team",
            "category",
            "category_name",
            "status",
            "budget_hours",
            "start_date",
            "end_date",
            "created_by",
            "created_by_name",
            "total_logged_hours",
            "task_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_by", "created_at", "updated_at"]

    def get_total_logged_hours(self, obj: Project) -> float:
        result = obj.time_entries.aggregate(total=Sum("hours"))
        return float(result["total"] or 0)

    def get_task_count(self, obj: Project) -> int:
        return obj.tasks.count()

    def create(self, validated_data: dict) -> Project:
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class ProjectTimeSummarySerializer(serializers.Serializer):
    """Read-only summary of time logged against a project."""

    total_hours = serializers.DecimalField(max_digits=10, decimal_places=2)
    billable_hours = serializers.DecimalField(max_digits=10, decimal_places=2)
    budget_hours = serializers.DecimalField(max_digits=8, decimal_places=2, allow_null=True)
    budget_remaining = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    entries_count = serializers.IntegerField()
