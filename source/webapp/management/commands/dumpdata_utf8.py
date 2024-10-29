import json
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Экспорт данных в JSON файл с кодировкой UTF-8"

    def handle(self, *args, **options):
        with open("fixtures/accoutns_data.json", "w", encoding="utf-8") as f:
            call_command(
                "dumpdata",
                "accounts",
                indent=4,
                format="json",
                natural_primary=True,
                natural_foreign=True,
                stdout=f,
            )
