from rest_framework import serializers
from core.models import User


class UserSerializer(serializers.ModelSerializer):
    
    re_password = serializers.CharField(
        write_only = True,
        style={"input_type" : "password"}
    )
    
    class Meta:
        
        model = User
        fields = ["id", "username", "first_name", "middle_name", "last_name", "email", "password", "re_password"]
        extra_kwargs = {
            "password" : {"write_only" : True, "style" : {"input_type" : "password"}},
        }
    
    