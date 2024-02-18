from rest_framework import serializers
from core.models import Team


class TeamSerializer(serializers.ModelSerializer):
    
    members = serializers.StringRelatedField(many=True)
    
    class Meta:
        
        model = Team
        fields = ["id", "profile", "name", "description", "members"]
        
    
    def get_members(self, instance):
        
        if instance:
            members_instance = instance.members.all()
            members = []
            
            for member in members_instance:
                members.append({
                    "id" : member.id,
                    "username" : member.username,
                    "first_name" : member.first_name,
                    "middle_name" : member.middle_name,
                    "last_name" : member.last_name,
                    "email" : member.email
                })
        
            return members
            
        else:
            return None        
    
    
    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        data["members"] = self.get_members(instance)
        return data
