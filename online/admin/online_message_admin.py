from django.contrib import admin
from django.core.checks import messages

from ..models import OnlineMessage
from ..tasks.upload_online_message_to_ghost import upload_online_message_to_ghost


@admin.register(OnlineMessage)
class OnlineMessageAdmin(admin.ModelAdmin):
    list_display = ['title', 'ghost_id', 'message_service_id']

    actions = [
        'upload_to_ghost',
    ]

    def upload_to_ghost(self, request, queryset):
        list(map(upload_online_message_to_ghost.delay, queryset.values_list('id', flat=True)))
        self.message_user(
            request=request,
            message=f'Создана задача на обновление постов',
            level=messages.INFO,
        )
