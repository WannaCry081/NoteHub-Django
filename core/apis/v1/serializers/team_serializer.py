from rest_framework import serializers
from core.models import Team


class TeamSerializer(serializers.ModelSerializer):
    
    members = serializers.StringRelatedField(many=True)
    
    class Meta:
        
        model = Team
        fields = ["id", "profile", "name", "description", "members"]
    
    
    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        data["members"] = self.get_members(instance)
        return data
