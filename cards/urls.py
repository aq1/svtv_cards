from django.urls import (
    path,
)

from .views import post_updated_webhook


urlpatterns = [
    path('webhook/post_updated/', post_updated_webhook, name='ghost_webhook_view'),
]
