"""TimeScoper URL configuration."""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    # API v1
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/teams/", include("apps.teams.urls")),
    path("api/v1/projects/", include("apps.projects.urls")),
    path("api/v1/tasks/", include("apps.tasks.urls")),
    path("api/v1/time-entries/", include("apps.timelog.urls")),
    path("api/v1/reports/", include("apps.reporting.urls")),
    # OpenAPI schema
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/v1/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
