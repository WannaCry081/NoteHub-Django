from django.contrib import admin
from api.models import *
from api.admins import *

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Team)
admin.site.register(Note)