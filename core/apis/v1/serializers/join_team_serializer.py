from rest_framework import serializers


class JoinTeamSerializer(serializers.Serializer):
    
    code = serializers.CharField(required = True)