from django.db import models 


class Note(models.Model):
    
    title = models.CharField(max_length = 100, unique = True, blank = False, null = False)
    body = models.TextField(blank = True, null = True)

    team = models.ForeignKey("Team", on_delete=models.CASCADE, blank = False)    
    owner = models.ForeignKey("User", on_delete=models.CASCADE, blank = False)
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    
    def __str__(self):
        return self.title