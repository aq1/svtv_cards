from django.urls import (
    path,
)

from .views import ghost_webhook_view


urlpatterns = [
    path('/webhook/', ghost_webhook_view, name='ghost_webhook_view'),
]
