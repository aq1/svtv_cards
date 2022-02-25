from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from ..models import PostBackup


@admin.register(PostBackup)
class PostBackupAdmin(SimpleHistoryAdmin):
    list_display = ['ghost_id', 'updated_at', 'title']
    ordering = ['-updated_at']
