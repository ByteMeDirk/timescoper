"""URL configuration for the teams app."""

from django.urls import path

from . import views

app_name = "teams"

urlpatterns = [
    path("", views.TeamListCreateView.as_view(), name="team-list"),
    path("<uuid:pk>/", views.TeamDetailView.as_view(), name="team-detail"),
    path("<uuid:team_pk>/members/", views.TeamMemberListView.as_view(), name="team-members"),
    path(
        "<uuid:team_pk>/members/<uuid:user_pk>/",
        views.TeamMemberRemoveView.as_view(),
        name="team-member-remove",
    ),
]
