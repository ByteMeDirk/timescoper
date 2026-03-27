"""Views for task management."""

from rest_framework import generics, permissions

from .models import Task, TaskComment
from .serializers import TaskCommentSerializer, TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    """List tasks or create a new one."""

    serializer_class = TaskSerializer
    filterset_fields = ["project", "assigned_to", "status", "priority", "parent_task"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "due_date", "priority", "status"]

    def get_queryset(self):
        return Task.objects.select_related(
            "project", "assigned_to", "created_by", "parent_task"
        ).prefetch_related("labels", "subtasks", "comments", "time_entries")


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a task."""

    serializer_class = TaskSerializer
    queryset = Task.objects.select_related(
        "project", "assigned_to", "created_by"
    ).prefetch_related("labels", "subtasks", "comments", "time_entries")


class TaskCommentListCreateView(generics.ListCreateAPIView):
    """List comments on a task or add a new one."""

    serializer_class = TaskCommentSerializer

    def get_queryset(self):
        return TaskComment.objects.filter(
            task_id=self.kwargs["task_pk"]
        ).select_related("author")

    def perform_create(self, serializer):
        serializer.save(task_id=self.kwargs["task_pk"])
