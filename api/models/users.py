from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    profile = models.URLField(blank = True)
    username = models.CharField(max_length = 100, unique = True)
    first_name = models.CharField(max_length = 40, blank = True, null = True)
    middle_name = models.CharField(max_length = 40, blank = True, null = True)
    last_name = models.CharField(max_length = 40, blank = True, null = True)
    email = models.EmailField(unique = True, blank = False, null = False)
    
    teams = models.ManyToManyField("Team", related_name="team_user", blank = True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    
    def __str__(self):
        return self.email