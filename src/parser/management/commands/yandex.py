from django.core.management import BaseCommand

from src.parser.yandex import yandex


class Command(BaseCommand):
    help = 'Parser news from Yandex News'

    def handle(self, *args, **options):
        yandex()
