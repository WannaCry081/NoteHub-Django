from django.contrib import admin
from core.models import *
from core.admins import *

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Team)