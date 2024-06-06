from rest_framework import serializers
from .models import FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):
    def validate_to_user(self, to_user):
        from_user = self.context["request"].user
        if to_user == from_user:
            raise serializers.ValidationError(
                "You can't send a friend request to yourself."
            )
        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            raise serializers.ValidationError(
                "You have already sent a friend request to this user."
            )
        if FriendRequest.objects.filter(from_user=to_user, to_user=from_user).exists():
            raise serializers.ValidationError(
                "That user already sent you a friend request."
            )
        return to_user

    class Meta:
        model = FriendRequest
        fields = (
            "id",
            "from_user",
            "to_user",
            "created_at",
            "accepted_at",
            "rejected_at",
        )
        read_only_fields = (
            "id",
            "from_user",
            "created_at",
            "accepted_at",
            "rejected_at",
        )
