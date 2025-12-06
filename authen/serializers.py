from rest_framework import serializers
from typing import Any
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login

from .models import CustomUser

# For user registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_pass = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "username",
            "password",
            "confirm_pass",
            "first_name",
            "last_name",
            "primary_lng",
            "pic"
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "confirm_pass": {"write_only": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_pass"]:
            raise serializers.ValidationError(
                {"confirm_pass": "Passwords do not match."}
            )
        return attrs
    def create(self, validated_data):
        validated_data.pop("confirm_pass")
        return CustomUser.objects.create_user(**validated_data)

# For user profile (read-only)
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "primary_lng",
            "pic",
            "is_searchable"
        ]

# For Custom Token serializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    token_class = RefreshToken

    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["uid"] = self.user.id
        data["username"] = self.user.username
        data["primary_lng"] = self.user.primary_lng
        
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

class PrivacySettingSerializer(serializers.Serializer):
    is_searchable = serializers.BooleanField(required=True)
