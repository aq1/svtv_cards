from django.shortcuts import redirect
from django.urls import (
    path,
)

from .views import (
    post_unpublished_webhook,
    post_published_webhook,
    post_updated_webhook,
)


urlpatterns = [
    path('post_updated/', post_updated_webhook, name='post_updated_webhook'),
    path('post_published/', post_published_webhook, name='post_published_webhook'),
    path('post_unpublished/', post_unpublished_webhook, name='post_unpublished_webhook'),
]
