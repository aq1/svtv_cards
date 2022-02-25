from django.contrib import admin

from ..models import OnlineMessage


@admin.register(OnlineMessage)
class OnlineMessageAdmin(admin.ModelAdmin):
    list_display = ['ghost_id', 'message_service_id', 'title']
