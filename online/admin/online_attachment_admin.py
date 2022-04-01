from django.contrib import admin

from ..models import OnlineAttachment


@admin.register(OnlineAttachment)
class OnlineAttachmentAdmin(admin.ModelAdmin):
    list_display = ['message', 'url', 'attachment_id']
