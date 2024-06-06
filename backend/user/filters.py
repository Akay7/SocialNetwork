from django.db.models import Q
from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model
from friend_request.models import FriendRequest

User = get_user_model()


class UserFilter(filters.FilterSet):
    is_friend = filters.BooleanFilter(method="filter_is_friend")

    def filter_is_friend(self, queryset, name, value):
        accepted_friend_requests = FriendRequest.objects.filter(
            accepted_at__isnull=False, rejected_at__isnull=True
        )
        requests_from_user = accepted_friend_requests.filter(
            from_user=self.request.user
        ).values_list("to_user")
        requests_to_user = accepted_friend_requests.filter(
            to_user=self.request.user
        ).values_list("from_user")
        query = Q(id__in=requests_from_user) | Q(id__in=requests_to_user)
        if value:
            return queryset.filter(query)
        else:
            return queryset.exclude(query).exclude(id=self.request.user.id)

    class Meta:
        model = User
        fields = ["is_friend"]
