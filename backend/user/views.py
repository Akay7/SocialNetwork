from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .serializers import UserSerializer
from .filters import UserFilter

User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View Users in the system.

    Possible to search by email, first name, and last name.

    To view only friends, use the is_friend filter.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ("=email", "first_name", "last_name")
    filterset_class = UserFilter
