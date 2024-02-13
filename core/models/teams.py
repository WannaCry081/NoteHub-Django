from django.db import models


class Team(models.Model):
    
    profile = models.URLField(blank = True)
    name = models.CharField(max_length = 20, unique = True)
    description = models.TextField(blank = True)
    
    members = models.ManyToManyField("User", related_name="user_team", blank = True)
    
    def __str__(self):
        return self.name