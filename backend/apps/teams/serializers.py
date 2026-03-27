"""Serializers for the teams app."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Team, TeamMembership

User = get_user_model()


class TeamMembershipSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = TeamMembership
        fields = ["id", "user", "user_email", "user_name", "role", "joined_at"]
        read_only_fields = ["id", "joined_at"]


class TeamSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(source="created_by.full_name", read_only=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "created_by",
            "created_by_name",
            "member_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_by", "created_at", "updated_at"]

    def get_member_count(self, obj: Team) -> int:
        return obj.memberships.count()

    def create(self, validated_data: dict) -> Team:
        validated_data["created_by"] = self.context["request"].user
        team = super().create(validated_data)
        # Auto-add creator as lead
        TeamMembership.objects.create(team=team, user=team.created_by, role="lead")
        return team


class AddMemberSerializer(serializers.Serializer):
    """Serializer for adding a member to a team."""

    user_id = serializers.UUIDField()
    role = serializers.ChoiceField(
        choices=TeamMembership._meta.get_field("role").choices,
        default="member",
    )

    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User not found.")
        return value
