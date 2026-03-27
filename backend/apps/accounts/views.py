"""Views for user registration and profile management."""

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .permissions import IsAdmin
from .serializers import AdminUserSerializer, RegisterSerializer, UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Register a new user account."""

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class MeView(generics.RetrieveUpdateAPIView):
    """Retrieve or update the authenticated user's own profile."""

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class AdminUserListView(generics.ListAPIView):
    """Admin-only: list all users in the system."""

    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    queryset = User.objects.all()
    filterset_fields = ["role", "is_active"]
    search_fields = ["email", "first_name", "last_name"]


class AdminUserDetailView(generics.RetrieveUpdateAPIView):
    """Admin-only: view and update any user (role, active status, etc.)."""

    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    queryset = User.objects.all()
