from rest_framework import serializers
from .models import FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):
    def validate_to_user(self, to_user):
        if to_user == self.context["request"].user:
            raise serializers.ValidationError(
                "You can't send a friend request to yourself."
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
