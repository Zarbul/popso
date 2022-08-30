from django.core.management import BaseCommand

from src.parser.ozon import ozon


class Command(BaseCommand):
    help = 'Parser news from Ozon news'

    def handle(self, *args, **options):
        ozon()
