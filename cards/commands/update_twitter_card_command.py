from ..utils import update_twitter_card


def update_twitter_card_command(post: dict, previous: dict):
    fields_to_watch = [
        'title',
        'feature_image',
        'status',
    ]

    if post['twitter_image']:
        if not any([r in previous for r in fields_to_watch]):
            return

    update_twitter_card.delay(post)
