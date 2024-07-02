from django.contrib import admin
from api.v1.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "short_body", "team", "created_at", "updated_at")
    search_fields = ("title", "body")

    def short_body(self, obj):
        words_limit = 10
        body = obj.body
        if len(body.split()) > words_limit:
            return " ".join(body.split()[:words_limit]) + "..."
        else:
            return body

    short_body.short_description = "Body"
