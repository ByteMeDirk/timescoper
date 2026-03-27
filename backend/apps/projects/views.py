"""Views for project management."""

from django.db.models import Q, Sum
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsTeamLeadOrAbove

from .models import Project
from .serializers import ProjectSerializer, ProjectTimeSummarySerializer


class ProjectListCreateView(generics.ListCreateAPIView):
    """List projects or create a new one."""

    serializer_class = ProjectSerializer
    filterset_fields = ["team", "status", "category"]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at", "start_date"]

    def get_queryset(self):
        return Project.objects.select_related(
            "team", "category", "created_by"
        ).prefetch_related("tasks", "time_entries")

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsTeamLeadOrAbove()]
        return [permissions.IsAuthenticated()]


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a project."""

    serializer_class = ProjectSerializer
    queryset = Project.objects.select_related("team", "category", "created_by")

    def get_permissions(self):
        if self.request.method in ("PATCH", "PUT", "DELETE"):
            return [permissions.IsAuthenticated(), IsTeamLeadOrAbove()]
        return [permissions.IsAuthenticated()]


class ProjectTimeSummaryView(APIView):
    """Return a time-logged summary for a single project."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found.", "code": "not_found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        agg = project.time_entries.aggregate(
            total_hours=Sum("hours"),
            billable_hours=Sum("hours", filter=Q(is_billable=True)),
        )
        total = agg["total_hours"] or 0
        billable = agg["billable_hours"] or 0
        budget = project.budget_hours
        remaining = (budget - total) if budget else None

        data = {
            "total_hours": total,
            "billable_hours": billable,
            "budget_hours": budget,
            "budget_remaining": remaining,
            "entries_count": project.time_entries.count(),
        }
        serializer = ProjectTimeSummarySerializer(data)
        return Response(serializer.data)
