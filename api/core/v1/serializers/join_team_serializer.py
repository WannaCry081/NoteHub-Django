import bleach
from rest_framework import serializers


class JoinTeamSerializer(serializers.Serializer):
    
    code = serializers.CharField(required = True)
    
    
    def validate(self, attrs):
        if "code" in attrs:
            attrs["code"] = bleach.clean(attrs["code"])
        
        return attrs