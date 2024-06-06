from django.contrib import admin
from .models import FriendRequest


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "from_user",
        "to_user",
        "created_at",
        "accepted_at",
        "rejected_at",
    ]
    search_fields = ["from_user__email", "to_user__email"]
    list_filter = ["accepted_at", "rejected_at"]
    ordering = ["id"]
