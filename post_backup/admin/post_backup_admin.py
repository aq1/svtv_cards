from django.contrib import admin

from ..models import PostBackup


@admin.register(PostBackup)
class PostBackupAdmin(admin.ModelAdmin):
    list_display = ['ghost_id', 'updated_at', 'title']
