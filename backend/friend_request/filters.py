from django_filters import rest_framework as filters

from friend_request.models import FriendRequest


class FriendRequestFilter(filters.FilterSet):
    is_received = filters.BooleanFilter(
        field_name="to_user", method="filter_is_received"
    )
    not_accepted = filters.BooleanFilter(field_name="accepted_at", lookup_expr="isnull")
    not_rejected = filters.BooleanFilter(field_name="rejected_at", lookup_expr="isnull")

    def filter_is_received(self, queryset, name, value):
        if value:
            return queryset.filter(to_user=self.request.user)
        else:
            return queryset.filter(from_user=self.request.user)

    class Meta:
        model = FriendRequest
        fields = ["is_received", "not_accepted", "not_rejected"]
