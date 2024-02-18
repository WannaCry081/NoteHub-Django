from django.db import models


class Team(models.Model):
    
    profile = models.URLField(blank = True, null = True)
    name = models.CharField(max_length = 20, unique = True)
    description = models.TextField(blank = True)
    
    members = models.ManyToManyField("User", related_name="user_team", blank = True)
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    
    def __str__(self):
        return self.name