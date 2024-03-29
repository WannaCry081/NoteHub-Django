from django.contrib import admin
from api.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "body", "created_at", "updated_at")
    search_fields = ("title", "body")