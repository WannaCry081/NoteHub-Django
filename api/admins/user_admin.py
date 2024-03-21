from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    
    def get_fieldsets(self, request, obj = None):
        
        fieldsets = super().get_fieldsets(request, obj)

        if obj:
            fieldsets = (
                (None, {"fields" : ("username", "email", "password")}),
                ("Personal info", {"fields" : ("first_name", "middle_name", "last_name", "teams")}),
            ) + fieldsets[2:]
            
        return fieldsets