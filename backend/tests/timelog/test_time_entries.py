"""Tests for time entry endpoints."""

from datetime import date
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model

from apps.projects.models import Project
from apps.teams.models import Team
from apps.timelog.models import TimeEntry

User = get_user_model()


@pytest.fixture
def team_and_project(team_lead_user):
    team = Team.objects.create(name="Backend", created_by=team_lead_user)
    project = Project.objects.create(
        name="API Build",
        team=team,
        created_by=team_lead_user,
        budget_hours=Decimal("100"),
    )
    return team, project


@pytest.mark.django_db
class TestTimeEntryCreation:
    URL = "/api/v1/time-entries/"

    def test_create_time_entry(self, auth_client, developer_user, team_and_project):
        _, project = team_and_project
        client = auth_client(developer_user)
        payload = {
            "project": str(project.id),
            "date": "2026-03-27",
            "hours": "4.5",
            "description": "Worked on API",
            "is_billable": True,
        }
        response = client.post(self.URL, payload, format="json")
        assert response.status_code == 201
        assert response.data["hours"] == "4.50"

    def test_rejects_over_24h_per_day(self, auth_client, developer_user, team_and_project):
        _, project = team_and_project
        client = auth_client(developer_user)

        # Log 20 hours
        TimeEntry.objects.create(
            user=developer_user,
            project=project,
            date=date(2026, 3, 27),
            hours=Decimal("20"),
        )
        # Try to log 5 more (total 25)
        payload = {
            "project": str(project.id),
            "date": "2026-03-27",
            "hours": "5",
        }
        response = client.post(self.URL, payload, format="json")
        assert response.status_code == 400


@pytest.mark.django_db
class TestMyDailyLog:
    URL = "/api/v1/time-entries/my-log/"

    def test_returns_own_entries(self, auth_client, developer_user, team_and_project):
        _, project = team_and_project
        TimeEntry.objects.create(
            user=developer_user,
            project=project,
            date=date(2026, 3, 27),
            hours=Decimal("3"),
        )
        client = auth_client(developer_user)
        response = client.get(f"{self.URL}?date=2026-03-27")
        assert response.status_code == 200
        assert len(response.data["results"]) == 1
