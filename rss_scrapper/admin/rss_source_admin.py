from django.contrib import admin

from ..models import RssFeed


@admin.register(RssFeed)
class RssFeedAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'last_updated_at', 'is_active']
