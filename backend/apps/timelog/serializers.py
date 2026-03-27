"""Serializers for the timelog app."""

from decimal import Decimal

from django.db.models import Sum
from rest_framework import serializers

from .models import TimeEntry


class TimeEntrySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)
    project_name = serializers.CharField(source="project.name", read_only=True)
    task_title = serializers.CharField(source="task.title", read_only=True, default=None)

    class Meta:
        model = TimeEntry
        fields = [
            "id",
            "user",
            "user_name",
            "task",
            "task_title",
            "project",
            "project_name",
            "description",
            "date",
            "hours",
            "is_billable",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def validate(self, attrs: dict) -> dict:
        """Ensure a user does not log more than 24 hours on a single date."""
        user = self.context["request"].user
        date = attrs.get("date")
        hours = attrs.get("hours", Decimal("0"))

        existing_qs = TimeEntry.objects.filter(user=user, date=date)
        if self.instance:
            existing_qs = existing_qs.exclude(pk=self.instance.pk)

        existing_total = existing_qs.aggregate(total=Sum("hours"))["total"] or Decimal("0")

        if existing_total + hours > Decimal("24"):
            raise serializers.ValidationError(
                {"hours": f"Total hours for {date} would exceed 24 ({existing_total} already logged)."}
            )
        return attrs

    def create(self, validated_data: dict) -> TimeEntry:
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
