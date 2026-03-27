"""URL configuration for the tasks app."""

from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.TaskListCreateView.as_view(), name="task-list"),
    path("<uuid:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path("<uuid:task_pk>/comments/", views.TaskCommentListCreateView.as_view(), name="task-comments"),
]
