"""Views for time entry management."""

from rest_framework import generics, permissions

from apps.accounts.permissions import IsOwnerOrTeamLeadOrAbove

from .models import TimeEntry
from .serializers import TimeEntrySerializer


class TimeEntryListCreateView(generics.ListCreateAPIView):
    """List time entries or log a new one."""

    serializer_class = TimeEntrySerializer
    filterset_fields = ["project", "task", "date", "is_billable", "user"]
    ordering_fields = ["date", "hours", "created_at"]

    def get_queryset(self):
        return TimeEntry.objects.select_related(
            "user", "task", "project"
        )


class TimeEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a time entry."""

    serializer_class = TimeEntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrTeamLeadOrAbove]
    queryset = TimeEntry.objects.select_related("user", "task", "project")


class MyDailyLogView(generics.ListAPIView):
    """Return the authenticated user's time entries for a given date."""

    serializer_class = TimeEntrySerializer

    def get_queryset(self):
        date = self.request.query_params.get("date")
        qs = TimeEntry.objects.filter(user=self.request.user).select_related("task", "project")
        if date:
            qs = qs.filter(date=date)
        return qs
