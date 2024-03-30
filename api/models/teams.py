from django.db import models
from api.utils import code_generator

class Team(models.Model):
    
    profile = models.URLField(blank = True, null = True)
    code = models.CharField(max_length = 8, default=code_generator, blank = False, null = False)
    name = models.CharField(max_length = 20, unique = True, blank = False, null = False)
    description = models.TextField(blank = True, null = True)
    
    owner = models.ForeignKey("User", on_delete=models.CASCADE)
    members = models.ManyToManyField("User", related_name="user_team", blank = True, null = True)
    notes = models.ManyToManyField("Note", related_name="team_notes", blank = True, null = True)
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    
    def __str__(self):
        return self.name