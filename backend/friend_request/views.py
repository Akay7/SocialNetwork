from django.utils import timezone
from django.db.models import Q
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import FriendRequest
from .serializers import FriendRequestSerializer
from .permissions import IsForCurrentUser
from .filters import FriendRequestFilter


class FriendRequestViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    filterset_class = FriendRequestFilter

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(from_user=self.request.user) | Q(to_user=self.request.user))
        )

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsForCurrentUser],
    )
    def accept(self, request, pk=None):
        friend_request = self.get_object()
        friend_request.accepted_at = timezone.now()
        friend_request.rejected_at = None
        friend_request.save(update_fields=["accepted_at", "rejected_at"])
        serializer = self.get_serializer(friend_request)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsForCurrentUser],
    )
    def reject(self, request, pk=None):
        friend_request = self.get_object()
        friend_request.rejected_at = timezone.now()
        friend_request.save(update_fields=["rejected_at"])
        serializer = self.get_serializer(friend_request)
        return Response(serializer.data)
