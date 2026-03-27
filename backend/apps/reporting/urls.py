"""URL configuration for the reporting app."""

from django.urls import path

from . import views

app_name = "reporting"

urlpatterns = [
    path("daily-summary/", views.DailySummaryView.as_view(), name="daily-summary"),
    path("weekly-summary/", views.WeeklySummaryView.as_view(), name="weekly-summary"),
    path("project-utilisation/", views.ProjectUtilisationView.as_view(), name="project-utilisation"),
    path("team-activity/", views.TeamActivityView.as_view(), name="team-activity"),
]
