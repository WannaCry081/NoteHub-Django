import bleach
from rest_framework import serializers
from api.models import Note


class NoteSerializer(serializers.ModelSerializer):
    
    team = serializers.StringRelatedField()
    owner = serializers.StringRelatedField()
    
    class Meta:
        
        model = Note
        fields = ["id", "title", "body", "team", "owner"]
        extra_kwargs = {
            "team" : {"read_only" : True},
            "owner" : {"read_only" : True},
        }
        
    
    def validate(self, attrs):
        
        if "owner" in attrs:
            attrs["owner"] = bleach.clean(attrs["owner"])
        if "team" in attrs:
            attrs["team"] = bleach.clean(attrs["team"])
        
        return attrs
    
    
    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        
        
        return data
    
    
    def get_owner(self, instance):
        
        if instance:
            owner_instance = instance.owner
            return {
                "id" : owner_instance.id,
                "email" : owner_instance.email,
                "username" : owner_instance.username
            }
        
        return None