from rest_framework import viewsets
from django.db.models import Q
from .models import FriendRequest
from .serializers import FriendRequestSerializer


class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(from_user=self.request.user) | Q(to_user=self.request.user))
        )

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)
