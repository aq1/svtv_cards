from django.http import HttpResponse, HttpRequest
from cards.commands import update_twitter_card_command
from .ghost_webhook_view import ghost_webhook_view


@ghost_webhook_view
def post_updated_webhook(request: HttpRequest, post, previous) -> HttpResponse:
    update_twitter_card_command(post, previous)
    return HttpResponse()