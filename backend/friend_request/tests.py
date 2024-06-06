import pytest
from user.tests.fixtures import UserFactory
from friend_request.models import FriendRequest
import factory


class FriendRequestFactory(factory.django.DjangoModelFactory):
    from_user = factory.SubFactory(UserFactory)
    to_user = factory.SubFactory(UserFactory)

    class Meta:
        model = FriendRequest


@pytest.fixture
def another_user():
    return UserFactory()


def test_review_friend_requests(authenticated_client, user):
    response = authenticated_client.get("/api/friend-request/")

    assert response.status_code == 200
    assert response.data["count"] == 0
    assert len(response.data["results"]) == 0


def test_cant_review_friend_requests_of_other_users(authenticated_client, user):
    FriendRequestFactory.create_batch(3)

    response = authenticated_client.get("/api/friend-request/")

    assert response.status_code == 200
    assert response.data["count"] == 0
    assert len(response.data["results"]) == 0


def test_can_create_friend_request(authenticated_client, user, another_user):
    response = authenticated_client.post(
        "/api/friend-request/",
        {
            "to_user": another_user.id,
        },
    )

    assert response.status_code == 201
    assert response.data["from_user"] == user.id
    assert response.data["to_user"] == another_user.id
    assert response.data["created_at"]
    assert response.data["rejected_at"] is None
    assert response.data["accepted_at"] is None


def test_can_review_created_requests(authenticated_client, user, another_user):
    friend_request = FriendRequestFactory(from_user=user, to_user=another_user)

    response = authenticated_client.get("/api/friend-request/")

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["from_user"] == user.id
    assert response.data["results"][0]["id"] == str(friend_request.id)


def test_can_review_request_to_user(authenticated_client, user, another_user):
    friend_request = FriendRequestFactory(from_user=another_user, to_user=user)

    response = authenticated_client.get("/api/friend-request/")

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["to_user"] == user.id
    assert response.data["results"][0]["id"] == str(friend_request.id)


def test_cant_create_request_to_user_itself(authenticated_client, user):
    response = authenticated_client.post(
        "/api/friend-request/",
        {
            "to_user": user.id,
        },
    )

    assert response.status_code == 400
    assert response.data == {
        "to_user": ["You can't send a friend request to yourself."]
    }


def test_cant_create_second_request_to_user(authenticated_client, user, another_user):
    FriendRequestFactory(from_user=user, to_user=another_user)

    response = authenticated_client.post(
        "/api/friend-request/",
        {
            "to_user": another_user.id,
        },
    )

    assert response.status_code == 400
    assert response.data["to_user"] == [
        "You have already sent a friend request to this user."
    ]


def test_cant_create_second_request_to_user_that_send_request(
    authenticated_client, user, another_user
):
    FriendRequestFactory(from_user=another_user, to_user=user)

    response = authenticated_client.post(
        "/api/friend-request/",
        {
            "to_user": another_user.id,
        },
    )

    assert response.status_code == 400
    assert response.data["to_user"] == ["That user already sent you a friend request."]


def test_can_accept_friend_request(authenticated_client, user):
    friend_request = FriendRequestFactory(to_user=user)
    assert not friend_request.accepted_at

    response = authenticated_client.post(
        f"/api/friend-request/{friend_request.id}/accept/"
    )

    assert response.status_code == 200
    assert response.data["id"] == str(friend_request.id)
    assert response.data["to_user"] == user.id
    assert response.data["created_at"]
    assert response.data["accepted_at"]
    friend_request.refresh_from_db()
    assert friend_request.accepted_at


def test_can_reject_friend_request(authenticated_client, user):
    friend_request = FriendRequestFactory(to_user=user)
    assert not friend_request.rejected_at

    response = authenticated_client.post(
        f"/api/friend-request/{friend_request.id}/reject/"
    )

    assert response.status_code == 200
    assert response.data["id"] == str(friend_request.id)
    assert response.data["to_user"] == user.id
    assert response.data["created_at"]
    assert response.data["rejected_at"]
    friend_request.refresh_from_db()
    assert friend_request.rejected_at
