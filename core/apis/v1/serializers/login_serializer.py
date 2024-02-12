# core/apis/v1/serializers.py
from rest_framework import serializers
from core.models import User


class LoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        style={"input_type": "password"}
    )

    