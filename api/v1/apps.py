from django.apps import AppConfig


class V1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.v1'

    def ready(self):
        from api.v1.admin import (
            UserAdmin,
            TeamAdmin,
            NoteAdmin,
        )  
