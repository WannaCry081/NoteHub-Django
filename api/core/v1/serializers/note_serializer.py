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
        
    