from django.contrib import admin

from ..models import OnlineMessage


@admin.register(OnlineMessage)
class OnlineMessageAdmin(admin.ModelAdmin):
    list_display = ['message_service_id', 'ghost_id', 'title']
