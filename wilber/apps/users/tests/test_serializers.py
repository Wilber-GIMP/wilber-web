from rest_framework import serializers

from apps.users.models import User
from apps.users.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    """
    Standard Serializer for User model.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "password",
            "last_login",
            "is_superuser",
            "username",
            "first_name",
            "last_name",
            "name",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
            "is_trusty",
        )


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Standard Serializer for UserProfile model.
    """

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "created",
            "modified",
            "user",
            "photo",
            "phone",
            "bio",
            "organization",
            "website",
            "facebook",
            "instagram",
            "birthday",
            "city",
            "country",
        )
