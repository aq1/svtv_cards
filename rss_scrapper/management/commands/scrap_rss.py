from django.core.management.base import BaseCommand

from rss_scrapper.tasks.scrap_rss import scrap_rss


class Command(BaseCommand):
    help = 'Scrap RSS'

    def handle(self, *args, **options):
        scrap_rss()
