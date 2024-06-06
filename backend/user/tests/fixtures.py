import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
import factory


User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")


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
