from django.http import HttpResponse, HttpRequest

from notifications.commands import notify_post_unpublished
from .ghost_webhook_view import ghost_webhook_view


@ghost_webhook_view
def post_unpublished_webhook(request: HttpRequest, post, previous) -> HttpResponse:
    notify_post_unpublished(post, previous)
    return HttpResponse()
