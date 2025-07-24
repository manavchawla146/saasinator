from django.contrib import admin
from .models import IdeaHistory

@admin.register(IdeaHistory)
class IdeaHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'idea', 'vibe', 'created_at')
    search_fields = ('idea', 'user__username', 'vibe')
    list_filter = ('vibe', 'created_at')