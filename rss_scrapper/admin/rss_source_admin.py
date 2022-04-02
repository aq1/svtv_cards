from django.contrib import admin

from ..models import RSSSource


@admin.register(RSSSource)
class RSSSourceAdmin(admin.ModelAdmin):
    list_display = ['url', 'last_updated_at', 'is_active']
