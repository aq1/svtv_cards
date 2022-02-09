from django.http import HttpResponse, HttpRequest

from cards.commands import update_post_fields_command
from .ghost_webhook_view import ghost_webhook_view


@ghost_webhook_view
def post_published_webhook(request: HttpRequest, post, previous) -> HttpResponse:
    update_post_fields_command(post, previous)
    return HttpResponse()
