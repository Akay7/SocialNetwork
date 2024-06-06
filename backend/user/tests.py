import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def email():
    return "user1@example.com"


@pytest.fixture
def password():
    return "safe11password"


@pytest.fixture
def user(django_user_model, email, password):
    return django_user_model.objects.create_user(email=email, password=password)


def authenticate_client(client, user):
    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(user).access_token}",
    )
    return client


@pytest.mark.django_db
def test_can_register_user(django_user_model, client, email, password):
    user_qty = django_user_model.objects.count()

    response = client.post(
        "/api/registration/",
        {
            "email": email,
            "password1": password,
            "password2": password,
        },
    )

    assert response.status_code == 201
    assert django_user_model.objects.count() == user_qty + 1


def test_can_login_as_user(user, client, email, password):
    response = client.post("/api/login/", {"email": email, "password": password})

    assert response.status_code == 200
    assert response.data["access"]
    assert response.data["refresh"]


def test_can_login_with_email_in_different_case(user, client, email, password):
    assert email != email.upper()

    response = client.post(
        "/api/login/", {"email": email.upper(), "password": password}
    )

    assert response.status_code == 200
    assert response.data["access"]
    assert response.data["refresh"]


def test_cant_register_with_email_in_different_case(user, client, password):
    assert user.email != user.email.upper()

    response = client.post(
        "/api/registration/",
        {
            "email": user.email.upper(),
            "password1": password,
            "password2": password,
        },
    )

    assert response.status_code == 400
    assert response.data["email"]


@pytest.mark.parametrize("authenticated", [True, False])
def test_authentication_is_mandatory(client, user, authenticated):
    if authenticated:
        authenticate_client(client, user)

    response = client.get("/api/users/")

    if authenticated:
        assert response.status_code == 200
    else:
        assert response.status_code == 401
