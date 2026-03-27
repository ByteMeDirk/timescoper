"""Tests for authentication and user management endpoints."""

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestRegistration:
    URL = "/api/v1/auth/register/"

    def test_register_creates_user(self, api_client):
        payload = {
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "securepass1",
            "password_confirm": "securepass1",
        }
        response = api_client.post(self.URL, payload, format="json")
        assert response.status_code == 201
        assert response.data["email"] == "new@example.com"
        assert User.objects.filter(email="new@example.com").exists()

    def test_register_rejects_mismatched_passwords(self, api_client):
        payload = {
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "securepass1",
            "password_confirm": "different",
        }
        response = api_client.post(self.URL, payload, format="json")
        assert response.status_code == 400

    def test_register_rejects_duplicate_email(self, api_client, developer_user):
        payload = {
            "email": "dev@example.com",
            "first_name": "Dup",
            "last_name": "User",
            "password": "securepass1",
            "password_confirm": "securepass1",
        }
        response = api_client.post(self.URL, payload, format="json")
        assert response.status_code == 400


@pytest.mark.django_db
class TestLogin:
    URL = "/api/v1/auth/login/"

    def test_login_returns_tokens(self, api_client, developer_user):
        response = api_client.post(
            self.URL,
            {"email": "dev@example.com", "password": "testpass123"},
            format="json",
        )
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_rejects_bad_credentials(self, api_client, developer_user):
        response = api_client.post(
            self.URL,
            {"email": "dev@example.com", "password": "wrong"},
            format="json",
        )
        assert response.status_code == 401


@pytest.mark.django_db
class TestMeEndpoint:
    URL = "/api/v1/auth/me/"

    def test_me_returns_profile(self, auth_client, developer_user):
        client = auth_client(developer_user)
        response = client.get(self.URL)
        assert response.status_code == 200
        assert response.data["email"] == "dev@example.com"

    def test_me_rejects_anonymous(self, api_client):
        response = api_client.get(self.URL)
        assert response.status_code == 401

    def test_me_update_profile(self, auth_client, developer_user):
        client = auth_client(developer_user)
        response = client.patch(self.URL, {"first_name": "Updated"}, format="json")
        assert response.status_code == 200
        assert response.data["first_name"] == "Updated"


@pytest.mark.django_db
class TestAdminUserEndpoints:
    LIST_URL = "/api/v1/auth/admin/users/"

    def test_admin_can_list_users(self, auth_client, admin_user, developer_user):
        client = auth_client(admin_user)
        response = client.get(self.LIST_URL)
        assert response.status_code == 200

    def test_developer_cannot_list_users(self, auth_client, developer_user):
        client = auth_client(developer_user)
        response = client.get(self.LIST_URL)
        assert response.status_code == 403
