import pytest
import factory
from user.tests.fixtures import UserFactory
from friend_request.models import FriendRequest


class FriendRequestFactory(factory.django.DjangoModelFactory):
    from_user = factory.SubFactory(UserFactory)
    to_user = factory.SubFactory(UserFactory)

    class Meta:
        model = FriendRequest


@pytest.fixture
def another_user():
    return UserFactory()
