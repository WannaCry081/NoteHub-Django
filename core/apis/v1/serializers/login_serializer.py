# core/apis/v1/serializers.py
from rest_framework import serializers
from core.models import User
from django.contrib.auth.hashers import check_password


class LoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        style={"input_type": "password"}
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials. Please try again.")

        if not check_password(password, user.password):
            raise serializers.ValidationError("Invalid credentials. Please try again.")

        attrs["user"] = user
        return attrs
