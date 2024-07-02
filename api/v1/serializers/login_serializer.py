import bleach
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from api.v1.models import User


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, style={"input_type": "password"})

    def validate(self, attrs):

        if "email" in attrs:
            attrs["email"] = bleach.clean(attrs["email"])

        if "password" in attrs:
            attrs["password"] = bleach.clean(attrs["password"])

        try:
            user = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials. Please try again.")

        if not check_password(attrs["password"], user.password):
            raise serializers.ValidationError("Invalid credentials. Please try again.")

        attrs["user"] = user
        return attrs
