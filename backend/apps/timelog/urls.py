"""URL configuration for the timelog app."""

from django.urls import path

from . import views

app_name = "timelog"

urlpatterns = [
    path("", views.TimeEntryListCreateView.as_view(), name="time-entry-list"),
    path("<uuid:pk>/", views.TimeEntryDetailView.as_view(), name="time-entry-detail"),
    path("my-log/", views.MyDailyLogView.as_view(), name="my-daily-log"),
]
