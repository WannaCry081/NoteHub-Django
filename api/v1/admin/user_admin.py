from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from api.v1.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    def get_fieldsets(self, request, obj=None):

        fieldsets = super().get_fieldsets(request, obj)

        if obj:
            fieldsets = (
                (None, {"fields": ("username", "email", "password")}),
                (
                    "Personal info",
                    {"fields": ("first_name", "middle_name", "last_name", "teams")},
                ),
            ) + fieldsets[2:]

        return fieldsets
