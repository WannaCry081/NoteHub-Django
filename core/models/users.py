from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    username = models.CharField(max_length = 100, unique = True)
    first_name = models.CharField(max_length = 40)
    middle_name = models.CharField(max_length = 40)
    last_name = models.CharField(max_length = 40)
    email = models.EmailField(unique = True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    
    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)