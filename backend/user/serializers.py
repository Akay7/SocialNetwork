from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
        ]


class EmailRegisterSerializer(RegisterSerializer):
    username = None

    def validate_email(self, email):
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("This email is already in use.")
        return super().validate_email(email)
