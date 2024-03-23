import bleach
from rest_framework import serializers
from api.models import Team


class TeamSerializer(serializers.ModelSerializer):
    
    owner = serializers.StringRelatedField(read_only = True)
    members = serializers.StringRelatedField(many=True, read_only = True)
    is_joined = serializers.SerializerMethodField(method_name="team_is_joined")

    class Meta:
        
        model = Team
        fields = ["id", "profile", "name", "code", "description", "owner", "is_joined", "members"]
        extra_kwargs = {
            "name" : {"read_only" : True},
            "owner" : {"read_only" : True},
            "code" : {"read_only" : True}
        }
        
        
    def __init__(self, *args, **kwargs):
        super(TeamSerializer, self).__init__(*args, **kwargs)
        
        exclude_fields = []
        
        if "exclude_fields" in kwargs.get("context"):
            exclude_fields.extend(kwargs.get("context").get("exclude_fields"))
            
        if exclude_fields is not None:
            for field in exclude_fields:
                self.fields.pop(field, None)
             
    
    def validate(request, attrs):
        
        if "profile" in attrs: 
            attrs["profile"] = bleach.clean(attrs["profile"])
        if "name" in attrs:
            attrs["name"] = bleach.clean(attrs["name"])
        if "description" in attrs:
            attrs["description"] = bleach.clean(attrs["description"])
            
        return attrs
    
    
    def get_owner(self, instance):
        
        if instance:
            owner_instance = instance.owner
            return {
                "id" : owner_instance.id,
                "username" : owner_instance.username,
                "email" : owner_instance.email,
            }
            
        else:
            return None
        
    
    def get_members(self, instance):
        
        if instance:
            members_instance = instance.members.all()
            members = []
            
            for member in members_instance:
                members.append({
                    "id" : member.id,
                    "username" : member.username,
                    "email" : member.email
                })
        
            return members
            
        else:
            return None        
    
    
    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        
        data["owner"] = self.get_owner(instance)
        data["members"] = self.get_members(instance) if data.get("is_joined") else []
            
        if "code" in data and self.context.get("request") and self.context["request"].method != "POST":
            del data["code"]
     
        return data

    
    def team_is_joined(self, team : Team):
        request = self.context.get("request")
        
        if request:
            user = request.user
            if user in team.members.all() or user == team.owner:
                return True
            
        return False    