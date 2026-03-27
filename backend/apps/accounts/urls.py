"""URL configuration for the accounts app."""

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("me/", views.MeView.as_view(), name="me"),
    # Admin endpoints
    path("admin/users/", views.AdminUserListView.as_view(), name="admin-user-list"),
    path(
        "admin/users/<uuid:pk>/",
        views.AdminUserDetailView.as_view(),
        name="admin-user-detail",
    ),
]
