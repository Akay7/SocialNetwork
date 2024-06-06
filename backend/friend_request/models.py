import uuid
from django.db import models


class FriendRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_user = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="friend_requests_sent",
    )
    to_user = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="friend_requests_received",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True)
    rejected_at = models.DateTimeField(null=True)

    class Meta:
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f"{self.from_user} -> {self.to_user}"
