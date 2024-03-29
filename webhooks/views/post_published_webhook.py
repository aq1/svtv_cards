from django.http import HttpResponse, HttpRequest

from cards.commands import update_post_fields_command
from notifications.commands import notify_post_published
from .ghost_webhook_view import ghost_webhook_view


@ghost_webhook_view
def post_published_webhook(request: HttpRequest, post, previous) -> HttpResponse:
    update_post_fields_command(post, previous)
    notify_post_published(post, previous)
    return HttpResponse()
