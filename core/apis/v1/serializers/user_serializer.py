import bleach
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
        
    
    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        
        exclude_fields = []
        request_method = self.context["request"].method if "request" in self.context else None
        
        if request_method in ["PATCH", "PUT"]:
            exclude_fields.extend(["re_password", "password"])

        for field_name in exclude_fields:
            self.fields.pop(field_name, None)
    
        
    def validate(self, attrs):

        if "username" in attrs:
            attrs["username"] = bleach.clean(attrs["username"])
        if "email" in attrs:
            attrs["email"] = bleach.clean(attrs["email"])
        if "first_name" in attrs:
            attrs["first_name"] = bleach.clean(attrs["first_name"])
        if "middle_name" in attrs:
            attrs["middle_name"] = bleach.clean(attrs["middle_name"])
        if "last_name" in attrs:
            attrs["last_name"] = bleach.clean(attrs["last_name"])
          
        if "password" in attrs and "re_password" in attrs: 
            if attrs["password"] != attrs["re_password"]:
                raise serializers.ValidationError("Invalid credentails. Please try again.")
    
        return attrs
    
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user