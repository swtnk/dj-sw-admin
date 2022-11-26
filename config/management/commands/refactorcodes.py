import subprocess
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = "Refactor and clean code"

    def handle(self, *args, **options):
        try:
            subprocess.run([f"{settings.BASE_DIR}/scripts/refactor_codes.sh"])
        except Exception as exc:
            raise CommandError(exc)
