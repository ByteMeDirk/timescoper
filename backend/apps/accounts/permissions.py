"""Reusable permission classes for role-based access control."""

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import UserRole


class IsAdmin(BasePermission):
    """Allow access only to users with the admin role."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(request.user and request.user.is_authenticated and request.user.role == UserRole.ADMIN)


class IsProjectManagerOrAbove(BasePermission):
    """Allow access to project managers and admins."""

    ALLOWED_ROLES = {UserRole.PROJECT_MANAGER, UserRole.ADMIN}

    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(request.user and request.user.is_authenticated and request.user.role in self.ALLOWED_ROLES)


class IsTeamLeadOrAbove(BasePermission):
    """Allow access to team leads, project managers, and admins."""

    ALLOWED_ROLES = {UserRole.TEAM_LEAD, UserRole.PROJECT_MANAGER, UserRole.ADMIN}

    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(request.user and request.user.is_authenticated and request.user.role in self.ALLOWED_ROLES)


class IsOwnerOrTeamLeadOrAbove(BasePermission):
    """
    Object-level permission: the resource owner, team leads, PMs, and admins
    may access. Requires the object to have a `user` or `created_by` FK.
    """

    ELEVATED_ROLES = {UserRole.TEAM_LEAD, UserRole.PROJECT_MANAGER, UserRole.ADMIN}

    def has_object_permission(self, request: Request, view: APIView, obj) -> bool:
        if request.user.role in self.ELEVATED_ROLES:
            return True
        owner = getattr(obj, "user", None) or getattr(obj, "created_by", None)
        return owner == request.user
