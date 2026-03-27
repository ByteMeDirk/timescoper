"""URL configuration for the projects app."""

from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("", views.ProjectListCreateView.as_view(), name="project-list"),
    path("<uuid:pk>/", views.ProjectDetailView.as_view(), name="project-detail"),
    path(
        "<uuid:pk>/time-summary/",
        views.ProjectTimeSummaryView.as_view(),
        name="project-time-summary",
    ),
]
