import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


def authenticate_client(client, user):
    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(user).access_token}",
    )
    return client


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def authenticated_client(user, client):
    return authenticate_client(client, user)


@pytest.fixture
def email():
    return "user1@example.com"


@pytest.fixture
def password():
    return "safe11password"


@pytest.fixture
def user(django_user_model, email, password):
    return django_user_model.objects.create_user(email=email, password=password)
