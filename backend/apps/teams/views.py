"""Views for team management."""

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.accounts.permissions import IsTeamLeadOrAbove

from .models import Team, TeamMembership
from .serializers import AddMemberSerializer, TeamMembershipSerializer, TeamSerializer

User = get_user_model()


class TeamListCreateView(generics.ListCreateAPIView):
    """List teams the user belongs to, or create a new team."""

    serializer_class = TeamSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role in ("admin", "project_manager"):
            return Team.objects.all().select_related("created_by")
        return Team.objects.filter(memberships__user=user).select_related("created_by").distinct()

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsTeamLeadOrAbove()]
        return [permissions.IsAuthenticated()]


class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a team."""

    serializer_class = TeamSerializer
    queryset = Team.objects.all().select_related("created_by")

    def get_permissions(self):
        if self.request.method in ("PATCH", "PUT", "DELETE"):
            return [permissions.IsAuthenticated(), IsTeamLeadOrAbove()]
        return [permissions.IsAuthenticated()]


class TeamMemberListView(generics.ListCreateAPIView):
    """List members of a team or add a new member."""

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddMemberSerializer
        return TeamMembershipSerializer

    def get_queryset(self):
        return TeamMembership.objects.filter(team_id=self.kwargs["team_pk"]).select_related("user")

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsTeamLeadOrAbove()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = AddMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        membership, created = TeamMembership.objects.get_or_create(
            team_id=self.kwargs["team_pk"],
            user_id=serializer.validated_data["user_id"],
            defaults={"role": serializer.validated_data["role"]},
        )
        if not created:
            return Response(
                {
                    "error": "User is already a member of this team.",
                    "code": "already_member",
                },
                status=status.HTTP_409_CONFLICT,
            )
        return Response(
            TeamMembershipSerializer(membership).data,
            status=status.HTTP_201_CREATED,
        )


class TeamMemberRemoveView(generics.DestroyAPIView):
    """Remove a member from a team."""

    permission_classes = [permissions.IsAuthenticated, IsTeamLeadOrAbove]

    def get_queryset(self):
        return TeamMembership.objects.filter(team_id=self.kwargs["team_pk"])

    def get_object(self):
        return self.get_queryset().get(user_id=self.kwargs["user_pk"])
