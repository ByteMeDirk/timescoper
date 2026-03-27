"""App configuration for timelog."""

from django.apps import AppConfig


class TimelogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.timelog"
    verbose_name = "Time Log"
