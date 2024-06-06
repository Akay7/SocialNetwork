from rest_framework import permissions


class IsForCurrentUser(permissions.BasePermission):
    message = "You can't neither accept nor decline your own friend request."

    def has_object_permission(self, request, view, obj):
        return obj.to_user == request.user
