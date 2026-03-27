"""Serializers for the tasks app."""

from rest_framework import serializers

from .models import Task, TaskComment, TaskLabel


class TaskLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskLabel
        fields = ["id", "name", "color_hex", "team", "created_at"]
        read_only_fields = ["id", "created_at"]


class TaskCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.full_name", read_only=True)
    author_email = serializers.EmailField(source="author.email", read_only=True)

    class Meta:
        model = TaskComment
        fields = ["id", "task", "author", "author_name", "author_email", "body", "created_at", "updated_at"]
        read_only_fields = ["id", "author", "created_at", "updated_at"]

    def create(self, validated_data: dict) -> TaskComment:
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)


class TaskSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(source="assigned_to.full_name", read_only=True, default=None)
    project_name = serializers.CharField(source="project.name", read_only=True)
    created_by_name = serializers.CharField(source="created_by.full_name", read_only=True)
    label_ids = serializers.PrimaryKeyRelatedField(
        queryset=TaskLabel.objects.all(),
        source="labels",
        many=True,
        required=False,
    )
    labels_detail = TaskLabelSerializer(source="labels", many=True, read_only=True)
    subtask_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    total_logged_hours = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "project",
            "project_name",
            "assigned_to",
            "assigned_to_name",
            "status",
            "priority",
            "estimated_hours",
            "due_date",
            "parent_task",
            "label_ids",
            "labels_detail",
            "subtask_count",
            "comment_count",
            "total_logged_hours",
            "created_by",
            "created_by_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]

    def get_subtask_count(self, obj: Task) -> int:
        return obj.subtasks.count()

    def get_comment_count(self, obj: Task) -> int:
        return obj.comments.count()

    def get_total_logged_hours(self, obj: Task) -> float:
        from django.db.models import Sum

        result = obj.time_entries.aggregate(total=Sum("hours"))
        return float(result["total"] or 0)

    def create(self, validated_data: dict) -> Task:
        labels = validated_data.pop("labels", [])
        validated_data["created_by"] = self.context["request"].user
        task = super().create(validated_data)
        if labels:
            task.labels.set(labels)
        return task

    def update(self, instance: Task, validated_data: dict) -> Task:
        labels = validated_data.pop("labels", None)
        task = super().update(instance, validated_data)
        if labels is not None:
            task.labels.set(labels)
        return task
