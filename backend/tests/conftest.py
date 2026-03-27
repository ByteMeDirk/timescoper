"""Shared test fixtures for the backend test suite."""

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def create_user(db):
    """Factory fixture for creating users with sensible defaults."""

    def _create(
        email: str = "dev@example.com",
        password: str = "testpass123",
        first_name: str = "Test",
        last_name: str = "User",
        role: str = "developer",
        **kwargs,
    ) -> User:
        return User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role,
            **kwargs,
        )

    return _create


@pytest.fixture
def developer_user(create_user):
    return create_user(email="dev@example.com", role="developer")


@pytest.fixture
def team_lead_user(create_user):
    return create_user(email="lead@example.com", role="team_lead", first_name="Team", last_name="Lead")


@pytest.fixture
def pm_user(create_user):
    return create_user(
        email="pm@example.com",
        role="project_manager",
        first_name="Project",
        last_name="Manager",
    )


@pytest.fixture
def admin_user(create_user):
    return create_user(email="admin@example.com", role="admin", first_name="Admin", last_name="User")


@pytest.fixture
def auth_client(api_client):
    """Return a function that authenticates an API client for a given user."""

    def _auth(user):
        api_client.force_authenticate(user=user)
        return api_client

    return _auth
