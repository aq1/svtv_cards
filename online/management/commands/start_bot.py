from django.core.management.base import BaseCommand

import online.channel_bot


class Command(BaseCommand):
    help = 'Starts channel bot'

    def handle(self, *args, **options):
        online.channel_bot.start()
