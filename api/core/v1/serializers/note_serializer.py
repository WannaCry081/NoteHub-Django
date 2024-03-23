from rest_framework import serializers
from api.models import Note


class NoteSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        
        model = Note
        fields = ["title", "body", "team"]
        extra_kwargs = {
            "team" : {"read_only" : True}
        }