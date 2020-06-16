import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    # So we can pass custom arguments and options to the command
    def handle(self, *args, **options):
        # Outputs a message to the screen
        self.stdout.write('Waiting for database...')

        # Holding the connection if available to check
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        # The self.style.SUCCESS prints a message in green
        self.stdout.write(self.style.SUCCESS('Database available'))
